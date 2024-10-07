
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q  # Ensure to import Q for complex queries
from .filters import UserGroupFilter  # Import your UserGroupFilter class
from django.contrib.auth.models import Group, User
from .filters import GroupFilter  # Import your filter class
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.models import Group, Permission
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .filters import UserFilter
from django_filters.views import FilterView
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from utils.decorators.permission_required import permissions_required
from users.models import Profile


# Create your views here.


def user_management(request):
    context = {'title': "User  Management", }

    return render(request, 'user_management/get_all.html', context)


@login_required
@permission_required("auth.view_user")
def user_list_view(request):
    # Exclude superusers from the queryset and fetch profiles
    queryset = User.objects.exclude(
        is_superuser=True).select_related('profile')

    # Get the search query from GET parameters
    email_query = request.GET.get('email', '')
    if email_query:
        queryset = queryset.filter(
            email__icontains=email_query)  # Filter by email

    # Order by username or any other field you prefer
    queryset = queryset.order_by('username')  # Explicitly order the queryset

    # Apply filtering using UserFilter
    user_filter = UserFilter(request.GET, queryset=queryset)
    filtered_queryset = user_filter.qs

    # Pagination logic
    paginator = Paginator(filtered_queryset, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user_management/get_all.html', {
        'page_obj': page_obj,
        'filter': user_filter,
    })


@login_required
@permissions_required("auth.add_user")
def add_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the password is provided
        if not password:
            messages.error(request, 'Password is required.')
            return redirect('user_list')

        # Check if a user with the same email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return redirect('user_list')

        try:
            # Create the user
            user = User.objects.create_user(
                username=email.split('@')[0],
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password  # Set the password
            )

            messages.success(request, 'User added successfully!')
            # log_action(request.user, ADDITION, f"Added New user for {
            #     request.user.username}", User)
            return redirect('user_list')

        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
            return redirect('user_list')

    return redirect('user_list')  # Redirect if not POST


# views.py


@login_required
@permissions_required("auth.delete_user")
def delete_user(request, user_id):
    # Get the user object or return a 404 error if not found
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Ensure that you don't delete the currently logged-in user
        if request.user == user:
            messages.error(request, "You cannot delete your own account.")
            # Redirect to the user list or appropriate page
            return redirect('user_list')

        user.delete()  # Delete the user
        messages.success(request, "User deleted successfully.")
      #   log_action(request.user, DELETION, f"Deleted user for {
      #       request.user.username}", User)
      #   log_action
        # Redirect to the user list or appropriate page
        return redirect('user_list')

    # If not a POST request, redirect to the user list
    return redirect('user_list')


@login_required
@permissions_required("auth.add_group")
def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        permissions = request.POST.getlist(
            'permissions')  # Get selected permissions

        # Check if the group already exists
        if Group.objects.filter(name=group_name).exists():
            messages.error(request, 'A group with this name already exists.')
            return redirect('create_group')

        # Create the new group
        group = Group.objects.create(name=group_name)

        # Assign selected permissions to the group
        for perm in permissions:
            permission = Permission.objects.get(id=perm)
            group.permissions.add(permission)

        messages.success(request, 'Group created successfully!')
        return redirect('list_groups')  # Redirect to an appropriate page

    # If not POST, render the form
    permissions = Permission.objects.all()  # Get all available permissions
    return render(request, 'user_management/create_group.html', {'permissions': permissions})


# views.py
@login_required
@permissions_required("auth.view_group")
def list_groups(request):
    group_filter = GroupFilter(
        request.GET, queryset=Group.objects.all().order_by('name'))
    paginator = Paginator(group_filter.qs, 10)  # Show 10 groups per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for group in page_obj:
        print("Group ID:", group.id)  # Debugging line

    return render(request, 'user_management/list_groups.html', {
        'filter': group_filter,
        'page_obj': page_obj,
    })


@login_required
@permissions_required("auth.delete_group")
def delete_group(request, group_id):
    print("Group Id :", group_id)
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Group deleted successfully!')
        return redirect('list_groups')  # Redirect to the group list

    return render(request, 'user_management/confirm_delete.html', {'group': group})


# views.py


@login_required
@permissions_required("auth.change_group")
def update_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        group_name = request.POST.get('group_name')

        # Update the group's name
        group.name = group_name

        # Get selected permissions from the form
        permissions = request.POST.getlist(
            'permissions')  # Retrieve selected permissions

        # Clear existing permissions and add new ones
        group.permissions.clear()
        for perm_id in permissions:
            permission = Permission.objects.get(id=perm_id)
            group.permissions.add(permission)

        group.save()
        messages.success(request, 'Group updated successfully!')
        return redirect('list_groups')  # Redirect to the group list

    # Get all available permissions for the form
    all_permissions = Permission.objects.all()

    # Get current permissions for the group
    current_permissions = group.permissions.all()

    return render(request, 'user_management/update_group.html', {
        'group': group,
        'all_permissions': all_permissions,
        'current_permissions': current_permissions,
    })


# views.py


@login_required
@permissions_required("auth.change_group")
def manage_group_users(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Apply the user filter
    user_filter = UserGroupFilter(request.GET, queryset=User.objects.all())

    if request.method == 'POST':
        user_ids_to_add = request.POST.getlist(
            'add_users')  # Get list of user IDs to add
        user_ids_to_remove = request.POST.getlist(
            'remove_users')  # Get list of user IDs to remove

        # Add users to the group
        for user_id in user_ids_to_add:
            user = get_object_or_404(User, id=user_id)
            group.user_set.add(user)
            messages.success(request, f'User {
                             user.username} added to the group.')

        # Remove users from the group
        for user_id in user_ids_to_remove:
            user = get_object_or_404(User, id=user_id)
            group.user_set.remove(user)
            messages.success(request, f'User {
                             user.username} removed from the group.')

        # Redirect to the same page
        return redirect('manage_group_users', group_id=group.id)

    # Get current members of the group
    current_members = group.user_set.all()

    return render(request, 'user_management/manage_group_users.html', {
        'group': group,
        'user_filter': user_filter,
        'current_members': current_members,
    })


# views.py


@login_required
@permissions_required("auth.view_group")
def list_groups_with_users(request):
    groups = Group.objects.all()  # Get all groups

    # Get the search query from the request
    search_query = request.GET.get('search', '')

    # Filter users based on the search query
    if search_query:
        users = User.objects.filter(
            Q(username__icontains=search_query) | Q(
                email__icontains=search_query)
        ).order_by('email')
    else:
        users = User.objects.all().order_by('email')  # If no search, show all users

    if request.method == 'POST':
        # Handle adding users to a group
        group_id = request.POST.get('group_id')
        user_ids_to_add = request.POST.getlist('add_users')
        user_ids_to_remove = request.POST.getlist('remove_users')

        group = get_object_or_404(Group, id=group_id)

        # Add users to the group
        for user_id in user_ids_to_add:
            user = get_object_or_404(User, id=user_id)
            group.user_set.add(user)
            messages.success(request, f'User {
                             user.username} added to the group {group.name}.')

        # Remove users from the group
        for user_id in user_ids_to_remove:
            user = get_object_or_404(User, id=user_id)
            group.user_set.remove(user)
            messages.success(request, f'User {
                             user.username} removed from the group {group.name}.')

        return redirect('list_groups_with_users')  # Redirect to the same page

    return render(request, 'user_management/list_groups_with_users.html', {
        'groups': groups,
        'users': users,
        'search_query': search_query,
    })
