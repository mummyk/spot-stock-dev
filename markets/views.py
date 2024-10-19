# views.py
from .models import InventoryItem
from .models import InventoryItem, Pack
from django.shortcuts import get_object_or_404
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError, FieldError
from django.contrib import messages
from utils.barcode_scanner import Barcode_scanner
from .forms import InventoryItemForm, CategoryForm, MeasurementForm, PackForm, RestockHistoryForm, SupplierInfoForm
from .models import InventoryItem, RestockHistory, Category, SupplierInfo, Pack, Measurement
from .filters import InventoryItemFilter, CategoryFilter, SupplierFilter, MeasurementFilter, PackageFilter, RestockingFilter, POSFilter
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
def inventory_list(request):
    """View to list inventory items with filtering and pagination."""
    inventory_items = InventoryItem.get_all_inventory()  # Get all inventory items

    # Apply filtering using django-filters
    item_filter = InventoryItemFilter(request.GET, queryset=inventory_items)

    item_filter_order = item_filter.qs.order_by(
        '-id')

   # Pagination logic
    paginator = Paginator(item_filter_order, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Inventory',
        'filter': item_filter,
        'inventory_items': page_obj,  # Use the paginated object here
    }

    return render(request, 'inventory/inventory_list.html', context)


@login_required
def category_list(request):
    """View to list category items with filtering and pagination."""
    inventory_items = Category.objects.all()  # Get all inventory items

    # Apply filtering using django-filters
    item_filter = CategoryFilter(request.GET, queryset=inventory_items)
    item_filter_order = item_filter.qs.order_by(
        '-id')

    # Pagination logic
    paginator = Paginator(item_filter_order, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Category',
        'filter': item_filter,
        'inventory_items': page_obj,  # Use the paginated object here
    }

    return render(request, 'inventory/category_list.html', context)


@login_required
def measurement_list(request):
    """View to list measurement items with filtering and pagination."""
    inventory_items = Measurement.objects.all()  # Get all inventory items

    # Apply filtering using django-filters
    item_filter = MeasurementFilter(request.GET, queryset=inventory_items)
    item_filter_order = item_filter.qs.order_by(
        '-id')

    # Pagination logic
    paginator = Paginator(item_filter_order, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Measurement',
        'filter': item_filter,
        'inventory_items': page_obj,  # Use the paginated object here
    }

    return render(request, 'inventory/measurement_list.html', context)


@login_required
def package_list(request):
    """View to list package items with filtering and pagination."""
    inventory_items = Pack.objects.all()  # Get all inventory items

    # Apply filtering using django-filters
    item_filter = PackageFilter(request.GET, queryset=inventory_items)
    item_filter_order = item_filter.qs.order_by(
        '-id')

    # Pagination logic
    paginator = Paginator(item_filter_order, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'package',
        'filter': item_filter,
        'inventory_items': page_obj,  # Use the paginated object here
    }

    return render(request, 'inventory/package_list.html', context)


@login_required
def restock_list(request):
    """View to list package items with filtering and pagination."""
    inventory_items = RestockHistory.objects.all()  # Get all inventory items

    # Apply filtering using django-filters
    item_filter = RestockingFilter(request.GET, queryset=inventory_items)
    item_filter_order = item_filter.qs.order_by(
        '-id')

    # Pagination logic
    paginator = Paginator(item_filter_order, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'package',
        'filter': item_filter,
        'inventory_items': page_obj,  # Use the paginated object here
    }

    return render(request, 'inventory/restock_list.html', context)


# views.py

@login_required
def scan_barcode(request):
    """View to scan barcode and check existence in inventory."""
    scanned_barcode = None  # Initialize variable to hold scanned barcode

    if request.method == 'POST':
        # Get the JSON data from the request body
        data = json.loads(request.body)
        barcode = data.get('barcode', '').strip()

        # Check if the barcode exists
        item_exists = InventoryItem.validate_barcode(barcode)

        if item_exists:
            scanned_barcode = barcode  # Store scanned barcode for rendering
            return JsonResponse({'exists': True, 'barcode': scanned_barcode})
        else:
            return JsonResponse({'exists': False, 'barcode': scanned_barcode})

    return render(request, 'inventory/scan_barcode.html', {'scanned_barcode': scanned_barcode, 'title': 'Scan Barcode'})


# views.py

@login_required
def sales(request):
    context = {'title': 'Sales'}
    return render(request, 'inventory/sales.html', context)


@login_required
def scan_barcode_sales(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. Only POST requests allowed.'}, status=405)

    try:
        data = json.loads(request.body)
        barcode = data.get('barcode', '').strip()

        inventory_item = InventoryItem.objects.filter(barcode=barcode).first()

        if inventory_item:
            if inventory_item.pack.id:
                pack = {'pack_id': str(inventory_item.pack.id) if inventory_item.pack else None,
                        'pack_price': str(inventory_item.pack.price_per_pack) if inventory_item.pack else None,
                        'pack_discount': str(inventory_item.pack.pack_discount) if inventory_item.pack else None, }
            else:
                pack = {}

            response_data = {
                'exists': True,
                'item_id': str(inventory_item.id),
                'name': inventory_item.name,
                'price': str(inventory_item.price),
                'discount': str(inventory_item.discount),
                'sku': inventory_item.sku,
                'pack': pack
            }
            # print('Inventory Data: ', response_data)

            return JsonResponse(response_data)
        else:
            return JsonResponse({'exists': False})

    except (json.JSONDecodeError, KeyError) as e:
        return JsonResponse({'error': f'Invalid JSON data: {str(e)}'}, status=400)

    except InventoryItem.DoesNotExist:
        return JsonResponse({'exists': False})

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


@login_required
def add_inventory_item(request, barcode):
    """View to add a new inventory item."""
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES)
        if form.is_valid():
            inventory_item = form.save(commit=False)
            inventory_item.user = request.user  # Set the logged-in user
            # inventory_item.barcode = barcode  # You can uncomment this if you want to set the barcode
            inventory_item.save()
            form.save_m2m()  # Save ManyToMany fields if any (e.g., categories)
            # Redirect to your inventory list or another page
            return redirect('inventory_list')
    else:
        # Pre-fill the barcode field
        form = InventoryItemForm(initial={'barcode': barcode})

    return render(request, 'inventory/add_inventory_item.html', {'form': form, 'barcode': barcode, 'title': 'Add Inventory'})


@login_required
def edit_inventory(request, inventory_id):
    """View to edit an existing inventory."""
    inventory = InventoryItem.objects.get(id=inventory_id)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            # Redirect to your measurement list or another page after successful edit
            return redirect('inventory_list')
    else:
        # Pre-fill the form with the measurement's existing data
        form = InventoryItemForm(instance=inventory)

    return render(request, 'inventory/add_inventory_item.html', {'form': form, 'title': 'Edit Category'})


@login_required
def delete_inventory(request, inventory_id):
    """View to delete a inventory."""
    try:
        inventory = Measurement.objects.get(id=inventory_id)
        inventory.delete()
        messages.success(request, f"Deleted measurement with id: {
                         inventory_id}")
        # Redirect to your measurement list or another page after successful deletion
        return redirect('inventory_list')
    except:
        raise ValidationError("Can't delete at the most recent measurement")


@login_required
def add_package(request, item_id):
    """View to add a new package for an inventory item."""

    # Get the single item object
    try:
        item = InventoryItem.objects.get(id=item_id)
        print("Item: ", item)
    except InventoryItem.DoesNotExist:
        # Handle the case where the item does not exist (optional)
        print("Inventory item not found.")
        messages.error(request, "Inventory item not found.")
        return redirect('inventory_list')

    if request.method == 'POST':
        form = PackForm(request.POST)
        if form.is_valid():
            print("After")
            package = form.save(commit=False)
            package.inventory_item = item  # Assign the item
            package.save()
            form.save_m2m()  # Save many-to-many fields if necessary
            # Redirect to your package list or another page
            return redirect('package_list')
        else:
            print("Form is not valid:", form.errors)
            error = form.errors

    else:
        print("Voild")
        # Pre-fill the inventory item in the form
        form = PackForm(initial={'inventory_item': item})
        error = form.errors

    return render(request, 'inventory/add_package.html', {
        'error': error,
        'form': form,
        'inventory_item': item,
        'title': 'Add Package',
        "ttype": True
    })


@login_required
def supplier_list(request):
    """View to list category items with filtering and pagination."""
    inventory_items = SupplierInfo.objects.all()  # Get all inventory items

    # Apply filtering using django-filters
    item_filter = SupplierFilter(request.GET, queryset=inventory_items)
    item_filter_order = item_filter.qs.order_by(
        '-id')

    # Pagination logic
    paginator = Paginator(item_filter_order, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Suppler list',
        'filter': item_filter,
        'inventory_items': page_obj,  # Use the paginated object here
    }

    return render(request, 'inventory/supplier_list.html', context)


@login_required
def add_suppliers(request):
    """View to add a new inventory item."""
    if request.method == 'POST':
        form = SupplierInfoForm(request.POST)
        if form.is_valid():
            supplier_info = form.save(commit=False)
            supplier_info.created_by = request.user  # Set the scanned barcode
            supplier_info.save()
            # Redirect to your inventory list or another page
            return redirect('supplier_list')

    else:
        # Pre-fill the barcode field
        form = SupplierInfoForm()

    return render(request, 'inventory/add_supplier.html', {'form': form, 'title': 'Add Suppliers', "ttype": True})


@login_required
def edit_supplier(request, supplier_id):
    """View to edit an existing category."""
    supplier = SupplierInfo.objects.get(id=supplier_id)
    if request.method == 'POST':
        form = SupplierInfoForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            # Redirect to your supplier list or another page after successful edit
            return redirect('supplier_list')
    else:
        # Pre-fill the form with the supplier's existing data
        form = SupplierInfoForm(instance=supplier)

    return render(request, 'inventory/add_supplier.html', {'form': form, 'title': 'Edit supplier'})


@login_required
def delete_supplier(request, supplier_id):
    """View to delete a supplier."""
    try:
        supplier = SupplierInfo.objects.get(id=supplier_id)
        supplier.delete()
        messages.success(request, f"Deleted supplier with id: {supplier_id}")
        # Redirect to your supplier list or another page after successful deletion
        return redirect('supplier_list')
    except:
        raise ValidationError("Can't delete at the most recent supplier")


@login_required
def add_categories(request):
    """View to add a new inventory item."""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.save(commit=False)
            category_name.save()
            # Redirect to your inventory list or another page
            return redirect('category_list')

    else:
        # Pre-fill the barcode field
        form = CategoryForm()

    return render(request, 'inventory/add_category.html', {'form': form, 'title': 'Add Category', 'ttype': True})


@login_required
def edit_categories(request, category_id):
    """View to edit an existing category."""
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            # Redirect to your category list or another page after successful edit
            return redirect('category_list')
    else:
        # Pre-fill the form with the category's existing data
        form = CategoryForm(instance=category)

    return render(request, 'inventory/add_category.html', {'form': form, 'title': 'Edit Category'})


@login_required
def delete_categories(request, category_id):
    """View to delete a category."""
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        messages.success(request, f"Deleted Category with id: {category_id}")
        # Redirect to your category list or another page after successful deletion
        return redirect('category_list')
    except:
        raise ValidationError("Can't delete at the most recent category")


@login_required
def add_measurement(request):
    """View to add a new inventory item."""
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.save()
            # Redirect to your inventory list or another page
            return redirect('measurement_list')

    else:
        # Pre-fill the  field
        form = MeasurementForm()

    return render(request, 'inventory/add_measurement.html', {'form': form, 'title': 'Add Measurement', "ttype": True})


@login_required
def edit_measurement(request, measurement_id):
    """View to edit an existing measurement."""
    measurement = Measurement.objects.get(id=measurement_id)
    if request.method == 'POST':
        form = MeasurementForm(request.POST, instance=measurement)
        if form.is_valid():
            form.save()
            # Redirect to your measurement list or another page after successful edit
            return redirect('measurement_list')
    else:
        # Pre-fill the form with the measurement's existing data
        form = MeasurementForm(instance=measurement)

    return render(request, 'inventory/add_measurement.html', {'form': form, 'title': 'Edit Category'})


@login_required
def delete_measurement(request, measurement_id):
    """View to delete a measurement."""
    try:
        measurement = Measurement.objects.get(id=measurement_id)
        measurement.delete()
        messages.success(request, f"Deleted measurement with id: {
                         measurement_id}")
        # Redirect to your measurement list or another page after successful deletion
        return redirect('measurement_list')
    except:
        raise ValidationError("Can't delete at the most recent measurement")


@login_required
def edit_pack(request, pack_id):
    """View to edit an existing pack."""
    pack = Pack.objects.get(id=pack_id)
    if request.method == 'POST':
        form = PackForm(request.POST, instance=pack)
        if form.is_valid():
            form.save()
            # Redirect to your pack list or another page after successful edit
            return redirect('package_list')
    else:
        # Pre-fill the form with the pack's existing data
        form = PackForm(instance=pack)

    return render(request, 'inventory/add_package.html', {'form': form, 'title': 'Edit Pack'})


@login_required
def delete_pack(request, pack_id):
    """View to delete a pack."""
    try:
        pack = Pack.objects.get(id=pack_id)
        pack.delete()
        messages.success(request, f"Deleted pack with id: {
                         pack_id}")
        # Redirect to your pack list or another page after successful deletion
        return redirect('package_list')
    except:
        raise ValidationError("Can't delete at the most recent pack")


@login_required
def restock_item(request, uuid):
    """View to handle item/pack restocking."""

    if request.method == 'POST':
        quantity_to_add = int(request.POST.get('quantity', 0))

        # First check if the uuid exists in InventoryItem
        try:
            # Try fetching the InventoryItem by UUID
            item = InventoryItem.objects.get(id=uuid)
            initial_quantity = item.quantity  # Save the initial quantity

            # Update the inventory item's quantity
            item.adjust_quantity(quantity_to_add)

            # Create a new RestockHistory entry
            RestockHistory.objects.create(
                type_added='inventory',
                initial_value=initial_quantity,
                uuid=uuid,
                restocked_by=request.user,
                quantity_added=quantity_to_add,
                restock_date=timezone.now()
            )
            messages.success(request, f'Successfully restocked {
                             item.name} by {quantity_to_add}')

        except InventoryItem.DoesNotExist:
            # If the uuid is not found in InventoryItem, convert it to an integer and check Pack
            try:
                # Try converting UUID to an integer and fetch Pack
                pack_id = int(uuid)
                pack = Pack.objects.get(id=pack_id)
                initial_quantity = pack.pack_quantity  # Save the initial pack quantity

                # Update the pack quantity
                pack.pack_quantity += quantity_to_add
                pack.save()

                # Create a new RestockHistory entry
                RestockHistory.objects.create(
                    type_added='pack',
                    initial_value=initial_quantity,
                    uuid=uuid,
                    restocked_by=request.user,
                    quantity_added=quantity_to_add,
                    restock_date=timezone.now()
                )
                messages.success(request, f'Successfully restocked pack for {
                                 pack.inventory_item.name} by {quantity_to_add}')

            except (Pack.DoesNotExist, ValueError):
                # Handle cases where the pack ID conversion fails or pack is not found
                messages.error(
                    request, 'Item not found in both InventoryItem and Pack')
                return redirect(request.META.get('HTTP_REFERER', 'inventory_list'))

        return redirect(request.META.get('HTTP_REFERER', 'inventory_list'))

    # If the method is not POST, redirect to inventory list
    messages.error(request, 'Invalid request method.')
    return redirect('inventory_list')


@login_required
def posSearch(request):
    inventory_items = InventoryItem.objects.all()  # Get all inventory items

    # Apply filtering using django-filters
    item_filter = POSFilter(request.GET, queryset=inventory_items)
    print('Checking: ', item_filter)
    filtered_items = item_filter.qs.order_by('-id')

    try:
        if filtered_items.exists():  # Check if any items exist
            # Iterate over each item in the queryset if there are multiple results
            for item in filtered_items:
                pack = {
                    'pack_id': str(item.pack.id) if item.pack else None,
                    'pack_price': str(item.pack.price_per_pack) if item.pack else None,
                    'pack_discount': str(item.pack.pack_discount) if item.pack else None,
                } if item.pack else {}

                response_data = {
                    'exists': True,
                    'item_id': str(item.id),
                    'name': item.name,
                    'price': str(item.price),
                    'discount': str(item.discount),
                    'sku': item.sku,
                    'pack': pack,
                }
                # print('Inventory Data: ', response_data)

                # Return the response for the first item found (you can customize as needed)
                return JsonResponse(response_data)
        else:
            return JsonResponse({'exists': False})

    except (json.JSONDecodeError, KeyError) as e:
        return JsonResponse({'error': f'Invalid JSON data: {str(e)}'}, status=400)

    except InventoryItem.DoesNotExist:
        return JsonResponse({'exists': False})

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)
