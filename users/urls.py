from django.urls import path
from .views import home, manage_profile, user_profile
urlpatterns = [
    path('', home, name='home'),
    path('profile/manage/', manage_profile, name='manage_profile'),
    path('profile/', user_profile, name='profile'),
]
