from django.urls import path
from .views import manage_profile, user_profile, manage_profile_image, delete_profile_image
urlpatterns = [
    path('profile/manage/', manage_profile, name='manage_profile'),
    path('profile/manage/images/', manage_profile_image,
         name='manage_profile_images'),
    path('profile/delete/', delete_profile_image, name='delete_profile_image'),
    path('profile/', user_profile, name='profile'),
]
