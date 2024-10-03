# Helper function to log actions

from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType


def log_action(user, action_flag, object_repr, obj=None):
    """
    A Log for every action on the system.

    If obj is None, skip logging the content type (this applies to actions where there's no associated object, such as failed signups).
    """
    if obj is not None:
        content_type = ContentType.objects.get_for_model(obj)
        object_id = obj.pk
    else:
        # If there is no object, set content_type and object_id to None
        content_type = None
        object_id = None

    LogEntry.objects.log_action(
        user_id=user.id,
        content_type_id=content_type.pk if content_type else None,
        object_id=object_id,
        object_repr=object_repr,
        action_flag=action_flag,
        change_message=f"{action_flag} performed by {user.username}"
    )
