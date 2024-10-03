from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from utils.decorators.permission_required import permissions_required
from utils.controller.getAllModel import get_all_models, get_choices


# Create your views here.


def home(request):
    if request.user.is_authenticated:
        print(get_choices())
        return redirect('dashboard')  # Redirect to dashboard if authenticated
    context = {'title': 'Home'}        # Pass the title to the template
    return render(request, 'home/index.html', context)


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    return render(request, 'errors/500.html', status=500)


def handler403(request, exception):
    return render(request, 'errors/403.html', status=403)


def handler400(request, exception):
    return render(request, 'errors/400.html', status=400)


# views.py


@login_required
@permissions_required("users.add_profile", "users.change_profile")
def manage_profile(request):
    # Get the user's profile or create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Update user first name and last name
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()  # Save user data

            form.save()  # Save profile data

            # Redirect to a profile view or another page
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    context = {'form': form, 'created': created}

    return render(request, 'profiles/manage_profile.html', context)

# views.py


@login_required
@permissions_required("users.view_profile")
def user_profile(request):
    try:

        profile = Profile.objects.get(user=request.user)
        if profile.profile_picture:
            profile_picture_url = request.build_absolute_uri(
                profile.profile_picture.url)
        else:
            profile_picture_url = request.build_absolute_uri(
                '/static/images/default_profile.png')
    except Profile.DoesNotExist:
        return redirect('manage_profile')

    return render(request, 'profiles/profile.html', {'profile': profile, 'iurl': profile_picture_url})
