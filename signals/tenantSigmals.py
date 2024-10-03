from django.dispatch import receiver
from django_tenants.models import TenantMixin
from django_tenants.signals import (
    schema_needs_to_be_sync,
    post_schema_sync,
    schema_migrated,
    schema_migrate_message
)
from django_tenants.utils import schema_context
from django_tenants.migration_executors.base import run_migrations


@receiver(schema_needs_to_be_sync, sender=TenantMixin)
def created_user_client_in_background(sender, **kwargs):
    client = kwargs['tenant']
    print("created_user_client_in_background %s" % client.schema_name)
    from clients.tasks import setup_tenant
    task = setup_tenant.delay(client)


@receiver(post_schema_sync, sender=TenantMixin)
def created_user_client(sender, **kwargs):
    client = kwargs['tenant']
    # send email to client to as tenant is ready to use


@receiver(schema_migrated, sender=run_migrations)
def handle_schema_migrated(sender, **kwargs):
    schema_name = kwargs['schema_name']
    # recreate materialized views in the schema


@receiver(schema_migrate_message, sender=run_migrations)
def handle_schema_migrate_message(**kwargs):
    message = kwargs['message']
    # recreate materialized views in the schema
