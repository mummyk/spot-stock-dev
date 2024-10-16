import requests
import json


class PaystackTransaction:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.url = 'https://api.paystack.co/transaction/initialize'
        self.verify_url = 'https://api.paystack.co/transaction/verify/'
        self.charge_url = 'https://api.paystack.co/transaction/charge_authorization'

    def _handle_response(self, response):
        """Handles API responses and raises exceptions for errors."""
        if response.status_code != 200:
            try:
                error_data = response.json()
                raise Exception(f"Error: {error_data['message']}")
            except json.JSONDecodeError:
                raise Exception("Error: Unable to decode response.")

        return response.json()

    def initialize_transaction(self, email, amount, callback_url, cancel_url):
        """ Initializes a transaction with the provided email and amount. """
        self.transaction_data = {
            "email": email,
            "amount": amount,  # Amount in kobo
            'callback_url': callback_url,
            'metadata': {
                "cancel_action": cancel_url
            }
        }

        headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json',
        }

        # Make the POST request
        response = requests.post(
            self.url, headers=headers, data=json.dumps(self.transaction_data))

        # Handle the response
        return self._handle_response(response)

    def transfer(self, email, amount, callback_url, cancel_url):
        """ Transfers the specified amount to the given email. """
        # Convert amount to kobo (1 Naira = 100 kobo)
        amount_in_kobo = amount * 100

        # Initialize the transaction and get the response
        try:
            response = self.initialize_transaction(
                email, amount_in_kobo, callback_url, cancel_url)
            if response["status"]:
                authorization_url = response["data"]["authorization_url"]
                access_code = response["data"]["access_code"]
                reference = response["data"]["reference"]

                print("Authorization URL:", authorization_url)
                print("Access Code:", access_code)
                print("Reference:", reference)

                return {
                    "authorization_url": authorization_url,
                    "access_code": access_code,
                    "reference": reference,
                }
            else:
                print("Failed to initialize transaction.")
                return None
        except Exception as e:
            print(f"Error during transfer: {e}")
            return None

    def verify_transaction(self, reference):
        """ Verifies a transaction using its reference. """
        url = f"{self.verify_url}{reference}"

        headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json',
        }

        # Make the GET request to verify the transaction
        response = requests.get(url, headers=headers)

        # Handle the response
        try:
            verification_data = self._handle_response(response)
            data = verification_data.get('data', {})

            transaction_info = {
                "id": data.get('id'),
                "status": data.get('status'),
                "amount": data.get('amount'),
                "currency": data.get('currency'),
                "paid_at": data.get('paid_at'),
                "gateway_response": data.get('gateway_response'),
                "customer_email": data['customer'].get('email'),
                "authorization_code": data['authorization'].get('authorization_code'),
                "fees": data.get('fees'),
                "reference": data.get('reference')
            }

            print("Transaction Information:")
            for key, value in transaction_info.items():
                print(f"{key}: {value}")

            return transaction_info  # Return extracted information if needed
        except Exception as e:
            print(f"Error verifying transaction: {e}")
            return None

    def charge_authorization(self, email, amount, authorization_code):
        """ Charges a card using an authorization code. """
        amount_in_kobo = amount * 100  # Convert amount to kobo

        charge_data = {
            "email": email,
            "amount": amount_in_kobo,
            "authorization_code": authorization_code,
        }

        headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json',
        }

        # Make the POST request to charge authorization
        response = requests.post(
            self.charge_url, headers=headers, data=json.dumps(charge_data))

        # Handle the response
        try:
            charge_response = self._handle_response(response)
            print("Charge successful:", charge_response)
            return charge_response  # Return charge details if needed
        except Exception as e:
            print(f"Error charging authorization: {e}")
            return None  # Return None or handle error as needed


# Example usage
# if __name__ == "__main__":
#     secret_key = 'YOUR_SECRET_KEY'  # Replace with your actual secret key

#     transaction = PaystackTransaction(secret_key)

#     # Step 1: Transfer example using an email and amount.
#     email = 'chibuzoi410@outlook.com'  # Customer's email
#     amount_to_transfer = 50             # Amount in Naira

#     transfer_response = transaction.transfer(email, amount_to_transfer)

#     if transfer_response:
#         reference = transfer_response['reference']

#         # Step 2: Verify the transaction using the reference.
#         verification_response = transaction.verify_transaction(reference)

#         if verification_response:
#             # Step 3: Charge again using the authorization code from verification.
#             authorization_code = verification_response['authorization']['authorization_code']

#             charge_amount = 50  # Amount in Naira to charge again

#             charge_response = transaction.charge_authorization(email, charge_amount, authorization_code)
