from .models import Wallet
from django.contrib.contenttypes.models import ContentType
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.apps import apps
from django.db import transaction
import logging

logger = logging.getLogger(__name__)


@receiver(user_signed_up)
def create_wallet(request, user, **kwargs):
    logger.info(f"Signal received: user_signed_up for user {
                user.username} and wallet created")

    try:
        with transaction.atomic():
            Wallet.objects.create(user=user)

    except Exception as e:
        print(str(e))
        # logger.error(f"Error in assign_user_to_member_group for user "
        #              f"{user.username}: {str(e)}")
