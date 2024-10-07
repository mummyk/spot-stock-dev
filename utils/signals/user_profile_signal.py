from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.apps import apps


@receiver(user_signed_up)
def assign_user_to_member_group(request, user, **kwargs):
    # Check if the group 'Member' exists; if not, create it
    group_name = "Member"
    member_group, created = Group.objects.get_or_create(name=group_name)

    if created:
        # If the group is created, assign all view, add, change, delete permissions for all models
        for app in apps.get_app_configs():
            for model in app.get_models():
                content_type = ContentType.objects.get_for_model(model)

                # List of permission codes we want to assign (view, add, change, delete)
                permissions_codes = ['view', 'add']

                # Loop over each permission and assign to the group
                for perm_code in permissions_codes:
                    permission = Permission.objects.filter(
                        content_type=content_type,
                        codename=f'{perm_code}_{model._meta.model_name}'
                    ).first()

                    if permission:
                        member_group.permissions.add(permission)

    # Add the user to the 'Member' group
    user.groups.add(member_group)
