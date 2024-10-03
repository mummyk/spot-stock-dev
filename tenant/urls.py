from django.urls import path
from .views import getCompanyList

urlpatterns = [
    path('list/', getCompanyList, name='list-company'),

]
