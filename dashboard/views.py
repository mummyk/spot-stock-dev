from django.shortcuts import render
from users.views import Profile

# Create your views here.


def dashboard(request):
    # Check if the user has a profile

    has_profile = Profile.objects.filter(user=request.user).exists()
    # Determine current theme
    current_theme = request.COOKIES.get(
        'theme', 'light')  # Default to light mode
    body_class = f"{current_theme}-mode"

    context = {'title': "Dashboard",
               'has_profile': has_profile, 'body_class': body_class, }
    return render(request, 'dashboard/dashboard.html', context)
