from .models import Client, Domain
from .forms import ClientForm
from .filters import ClientFilter
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator

# Create your views here.


# views.py


@login_required
def tenant_list_view(request):
    # Assuming you have a filter set up
    filter_set = ClientFilter(
        request.GET, queryset=Client.objects.all().order_by('name'))

    # Get the filtered queryset
    tenants = filter_set.qs

    # Set up pagination
    paginator = Paginator(tenants, 10)  # Show 10 tenants per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tenants/tenant_list.html', {
        'filter': filter_set,
        'page_obj': page_obj,
    })


@login_required
def tenant_create_view(request):
    if request.method == "POST":
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            schema_name = form.cleaned_data['schema_name']
            # Create the tenant using form data
            tenant = Client(
                schema_name=form.cleaned_data['schema_name'],
                name=form.cleaned_data['name'],
                country=form.cleaned_data['country'],
                city=form.cleaned_data['city'],
                owner=request.user,  # Set the owner to the logged-in user
                address=form.cleaned_data['address'],
                phone_number=form.cleaned_data['phone_number'],
                color=form.cleaned_data['color']
            )
            tenant.save()  # Save the tenant instance

            domain_sub = ''
            if schema_name == 'public':
                domain_sub = settings.BACKEND_URL
            else:
                domain_sub = f'{schema_name}.{settings.BACKEND_URL}'

            # Create the domain for this tenant
            domain = Domain()
            domain.domain = domain_sub  # Set your desired domain here
            domain.tenant = tenant
            domain.is_primary = True
            domain.save()

            # Redirect to tenant list after creation
            return redirect('tenant_list')
    else:
        form = ClientForm()

    return render(request, 'tenants/tenant_form.html', {'form': form})


@login_required
def tenant_edit_view(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            # Redirect to tenant list after editing
            return redirect('tenant_list')
    else:
        form = ClientForm(instance=client)

    return render(request, 'tenants/tenant_form.html', {'form': form})


@login_required
def tenant_delete_view(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        client.delete()
        # Redirect to tenant list after deletion
        return redirect('tenant_list')

    return render(request, 'tenants/tenant_confirm_delete.html', {'client': client})
