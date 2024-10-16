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
    path("", include("userMangment.urls")),
    path("", include("tenant.urls")),
    path("wallet/", include("wallet.urls")),
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
