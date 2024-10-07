from django.urls import path
from .views import company


urlpatterns = [
    path("company/", company, name="company"),
]
