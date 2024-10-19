from decimal import Decimal
from django.conf import settings
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import HttpResponse
import logging
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib import messages
from utils.paystack import PaystackTransaction
from .filters import UserFilter  # Import the updated UserFilter
from .models import Wallet, Transaction, Payment
from .filters import PaymentFilter, TransactionFilter


@login_required
def balance(request):
    try:
        # Check if the user has a wallet
        wallet = Wallet.objects.get(user=request.user)

        # Check if the wallet has a password
        if not wallet.password:
            if request.method == 'POST':
                # Ask user to create a password if none exists
                password = request.POST.get('password')
                if password:
                    wallet.set_password(password)
                    wallet.save()
                    return redirect('wallet_balance')
            return render(request, 'wallet/set_password.html', {'title': 'Set Wallet Password'})

        context = {'title': 'Wallet Balance',
                   'balance': wallet.balance}
        return render(request, 'wallet/balance.html', context)

        # else:
        #     # Wallet exists and has a password
        #     if request.method == 'POST':
        #         password = request.POST.get('password')
        #         if password and check_password(password, wallet.password):
        #             # Password is correct, show balance
        #             context = {'title': 'Wallet Balance',
        #                        'balance': wallet.balance}
        #             return render(request, 'wallet/balance.html', context)
        #         else:
        #             # Invalid password entered
        #             return render(request, 'wallet/verify_password.html', {'error': 'Invalid password', 'title': 'Verify Wallet Password'})
        #     return render(request, 'wallet/verify_password.html', {'title': 'Verify Wallet Password'})

    except Wallet.DoesNotExist:
        # Create a wallet if none exists
        if request.method == 'POST':
            password = request.POST.get('password')
            if password:
                wallet = Wallet.objects.create(user=request.user)
                wallet.set_password(password)
                wallet.save()
                return redirect('wallet_balance')
        return render(request, 'wallet/set_password.html', {'title': 'Set Wallet Password'})


@login_required
def deposit(request):
    """Handle the deposit view with password validation and row locking."""
    wallet = Wallet.objects.get(user=request.user)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        password = request.POST.get('password')
        payment_type = request.POST.get('payment_type')

        # Validate amount input
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValidationError("Amount must be greater than zero.")
        except (ValueError, TypeError, ValidationError):
            return render(request, 'wallet/deposit.html', {'error': 'Invalid amount entered.', 'title': 'Deposit'})

        try:
            if wallet.check_password(password):
                with transaction.atomic():
                    # Create a transaction
                    transactions = Transaction.objects.create(
                        wallet=wallet, transaction_type="deposit", amount=amount
                    )

                    # Create a payment linked to the transaction
                    payment = Payment.objects.create(
                        transaction=transactions, payment_method=payment_type
                    )

                    # Check payment type and initiate payment accordingly
                    # This will give you the base URL
                    # domain = request.build_absolute_uri('/')
                    domain = f"{request.scheme}://{request.get_host()}"

                    if payment_type == "paystack":
                        paystack = PaystackTransaction(
                            secret_key=settings.PAYSTACK_SECRET_KEY)
                        paystackTx = paystack.transfer(
                            request.user.email, amount, domain+settings.CALLBACK_URL, domain+settings.CANCEL_ACTION)
                        if paystackTx:
                            reference = paystackTx['reference']
                            authorization_url = paystackTx['authorization_url']
                            access_code = paystackTx['access_code']
                            payment.payment_reference = reference
                            payment.save()
                            context = {
                                'title': 'Verify Deposit',
                                'reference': reference,
                                'authorization_url': authorization_url,
                                'access_code': access_code
                            }

                            return render(request, 'wallet/verify_payment.html', context)

                    else:
                        raise ValidationError('Unsupported payment method.')

            else:
                raise ValidationError('Incorrect password.')

        except ValidationError as e:
            # Return error if there's any validation issue
            return render(request, 'wallet/deposit.html', {'error': str(e), 'title': 'Deposit'})

        except Exception as e:
            # Catch any other exceptions and display a generic error message
            return render(request, 'wallet/deposit.html', {'error': 'An unexpected error {e} occurred. Please try again later.', 'title': 'Deposit'})

    context = {'title': 'Deposit'}
    return render(request, 'wallet/deposit.html', context)


@login_required
def withdraw(request):
    """Handle the withdraw view with password validation and row locking."""
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        password = request.POST.get('password')

        try:
            with transaction.atomic():
                # Get the user's wallet
                wallet, created = Wallet.objects.get_or_create(
                    user=request.user)

                # Call the withdraw method in the Wallet model
                wallet.withdraw(amount, password)

                # Record the transaction
                Transaction.objects.create(
                    wallet=wallet, transaction_type='withdraw', amount=amount
                )
            return redirect('wallet_balance')

        except ValidationError as e:
            # Return error if there's any validation issue
            return render(request, 'wallet/withdraw.html', {'error': e.messages[0], 'title': 'withdraw'})

    context = {'title': 'withdraw'}
    return render(request, 'wallet/withdraw.html', context)


@login_required
def transfer(request):
    if request.method == 'GET':
        print('Searching')
        # Handle the filtering of users via the GET request
        # Use request.GET for filtering
        user_filter = UserFilter(request.GET, request=request)
        users = user_filter.qs  # Get the filtered queryset of users

        return render(request, 'wallet/transfer.html', {'users': users, 'filter': user_filter})

    # In case no POST or GET filtering, still pass the filter object
    user_filter = UserFilter(request=request)
    return render(request, 'wallet/transfer.html', {'filter': user_filter})


@login_required
def verify_wallet_transfer(request, user_id):
    """Handle the verification of a wallet transfer."""
    if request.method == 'POST':
        # Extract the transfer details from the request
        try:
            to_user_id = user_id
            amount = Decimal(request.POST.get('amount'))
            password = request.POST.get('password')

            print('Transferring')
            print('my id: ', request.user.id)
            print('rec id: ', to_user_id)

            # Verify the password
            sender_wallet = get_object_or_404(Wallet, user=request.user)
            if not sender_wallet.check_password(password):
                return render(request, 'wallet/verify_wallet_transfer.html', {'error': 'Invalid password'})

            # Get recipient's wallet
            recipient = get_object_or_404(User, id=to_user_id)
            recipient_wallet = get_object_or_404(Wallet, user=recipient)
            print('Receiver Wallet: %s' % recipient_wallet)

            # Ensure sufficient balance
            if sender_wallet.balance < amount:
                user_filter = UserFilter(request=request)
                return render(request, 'wallet/verify_wallet_transfer.html', {'error': 'Insufficient balance', 'filter': user_filter})

            with transaction.atomic():
                # Withdraw from sender's wallet
                # This should handle balance checks internally
                sender_wallet.withdraw(amount=amount, password=password)

                # Create a transaction record for the sender
                transaction_record = Transaction.objects.create(
                    wallet=sender_wallet,
                    transaction_type='transfer',
                    amount=amount,
                )

                # Create a payment record for this transaction
                payment_record = Payment.objects.create(
                    transaction=transaction_record,
                    payment_method='wallet'
                )

                # Deposit into recipient's wallet
                recipient_wallet.deposit(amount=amount)

                # Update payment record status and timestamp
                payment_record.processed_at = timezone.now()
                payment_record.status = "success"
                payment_record.save()

                return render(request, 'wallet/balance.html', {'success': 'Transfer completed successfully', "balance": sender_wallet.balance})

        except Exception as e:
            user_filter = UserFilter(request=request)
            return render(request, 'wallet/verify_wallet_transfer.html', {'error': str(e)})
    # If not a POST request, redirect or render an appropriate response
    # Redirect to the transfer page if not a POST request
    return render(request, 'wallet/verify_wallet_transfer.html', {'title': "Verify Wallet Transaction"})


@login_required
def fund_wallet_manual(request):
    """Handle wallet funding via manual cash or bank transfer."""
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        # 'cash' or 'bank_transfer'
        payment_method = request.POST['payment_method']
        description = request.POST.get('description', 'Manual wallet funding')

        if payment_method not in ['cash', 'bank_transfer']:
            return render(request, 'wallet/fund_wallet_manual.html', {'error': 'Invalid payment method selected.'})

        try:
            with transaction.atomic():
                # Log the manual transaction as a deposit (wallet funding)
                wallet = Wallet.objects.select_for_update().get(user=request.user)
                wallet.deposit(amount)  # Increase wallet balance

                # Log the transaction
                transaction_record = Transaction.objects.create(
                    wallet=wallet,
                    transaction_type='deposit',  # Indicating it's a wallet funding
                    payment_method=payment_method,  # 'cash' or 'bank_transfer'
                    amount=amount,
                    description=description
                )

                # Log the payment details
                Payment.objects.create(
                    transaction=transaction_record,
                    payment_method=payment_method,
                    status='completed'
                )

            return redirect('wallet_balance')

        except ValidationError as e:
            return render(request, 'wallet/fund_wallet_manual.html', {'error': str(e)})

    return render(request, 'wallet/fund_wallet_manual.html')


@login_required
def verify_transaction(request):
    # Get the `trxref` and `reference` from the query parameters
    trxref = request.GET.get('trxref')
    reference = request.GET.get('reference')

    if not reference:
        return HttpResponse("Reference not provided", status=400)

    # Create a PaystackTransaction instance
    paystack = PaystackTransaction(secret_key=settings.PAYSTACK_SECRET_KEY)

    try:
        # Verify the transaction with Paystack
        paystack_verify = paystack.verify_transaction(reference)
        print(paystack_verify)  # Print the response for debugging purposes

        # Extract necessary data from the Paystack response
        # This will be 'success' or other statuses
        status = paystack_verify.get('status')
        processed_at = paystack_verify.get('paid_at')  # Get the payment date
        authorization_code = paystack_verify.get('authorization_code')
        amount = paystack_verify.get('amount')
        customer_email = paystack_verify.get('customer_email')

        # Fetch the Payment record
        payment = get_object_or_404(Payment, payment_reference=reference)

        # Update the Payment model fields
        payment.status = status
        payment.processed_at = processed_at  # Set the 'processed_at' field
        payment.authorization_code = authorization_code  # Store the authorization code

        payment.save()

        if status == "success":
            # deposit to wallet
            wallet = payment.transaction.wallet
            wallet.deposit(amount=amount)

        messages.info(request, "Transaction is {status}.")

        return redirect('wallet_balance')

    except Payment.DoesNotExist:
        return HttpResponse("Payment record not found.", status=404)

    except Exception as e:
        print(f"An error occurred: {e}")
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


@login_required
def cancel_transaction(request):
    # Add a success message
    messages.success(request, "Transaction has been canceled successfully.")

    # Redirect to the wallet balance page
    return redirect("wallet_balance")


@login_required
def transaction_history(request):
    # Filter transactions by logged-in user’s wallet
    transactions = Transaction.objects.filter(wallet__user=request.user)

    # Apply the transaction filter to the queryset
    transaction_filter = TransactionFilter(request.GET, queryset=transactions)

    # Order the transactions by a relevant field (e.g., '-created_at' for most recent first)
    ordered_transactions = transaction_filter.qs.order_by(
        '-id')  # or 'created_at' if you have that field

    # Pagination logic: Show 10 transactions per page
    paginator = Paginator(ordered_transactions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': transaction_filter,
        'transactions': page_obj,  # Use the paginated and ordered transactions
    }

    return render(request, 'wallet/transaction_history.html', context)


@login_required
def payment_history(request):
    # Filter by logged-in user’s wallet
    payments = Payment.objects.filter(transaction__wallet__user=request.user)
    payment_filter = PaymentFilter(request.GET, queryset=payments)
    ordered_payment = payment_filter.qs.order_by(
        '-id')

    # Pagination logic
    paginator = Paginator(ordered_payment, 10)  # Show 10 payments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': payment_filter,
        'payments': page_obj,  # Use the paginated object here
    }
    return render(request, 'wallet/payment_history.html', context)
