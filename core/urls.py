"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static  # Remove when removing TODO
from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path("accounts/", include("allauth.urls")),
    path("", include("users.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("", include("userMangement.urls")),
    path("", include("tenant.urls")),
]

# TODO : Remenber to change to A server for production
# In development, serve media files with Django
# if settings.DEBUG:
#     from django.conf.urls.static import static
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

# Add the custom error handlers
handler404 = 'home.views.handler404'
handler500 = 'home.views.handler500'
handler403 = 'home.views.handler403'
handler400 = 'home.views.handler400'
