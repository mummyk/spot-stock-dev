# urls.py
from django.urls import path
from .views import (
    tenant_list_view, tenant_create_view,
    tenant_edit_view,
    tenant_delete_view,
)

urlpatterns = [
    path('tenants/', tenant_list_view, name='tenant_list'),
    path('tenants/create/', tenant_create_view, name='tenant_create'),
    path('tenants/edit/<int:pk>/', tenant_edit_view, name='tenant_edit'),
    path('tenants/delete/<int:pk>/', tenant_delete_view, name='tenant_delete'),
]
