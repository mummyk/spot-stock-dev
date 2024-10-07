from django.shortcuts import render
from users.views import Profile

# Create your views here.


def dashboard(request):
    # Check if the user has a profile

    has_profile = Profile.objects.filter(user=request.user).exists()

    context = {'title': "Dashboard",
               'has_profile': has_profile, }
    return render(request, 'dashboard/dashboard.html', context)
