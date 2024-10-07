from django.urls import path
from .views import user_management, user_list_view, add_user, delete_user, create_group, list_groups, delete_group, update_group, manage_group_users, list_groups_with_users


urlpatterns = [
    path("user-management/", user_management, name="user-management"),
    path('users-list/', user_list_view, name='user_list'),
    path('add-user/', add_user, name='add_user'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('create-group/', create_group, name='create_group'),
    path('groups/', list_groups, name='list_groups'),  # List all groups
    path('delete-group/<int:group_id>/', delete_group,
         name='delete_group'),  # Delete a specific group
    path('update-group/<int:group_id>/', update_group,
         name='update_group'),  # Update a specific group
    path('groups/manage-users/',
         list_groups_with_users, name='list_groups_with_users'),
]
