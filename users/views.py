from .models import Profile
from .forms import ProfileForm, Profile_pictureForm, ProfileFormLite
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from utils.decorators.permission_required import permissions_required
from utils.controller.getAllModel import get_all_models, get_choices
from django.contrib import messages
from utils.log_action import log_action
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
# Create your views here.


@login_required
@permissions_required("users.add_profile", "users.change_profile")
def manage_profile(request):
    # Get the user's profile or create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileFormLite(request.POST, instance=profile)
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


# Update or add Profile Picture
@login_required
@permissions_required("users.add_profile", "users.change_profile")
def manage_profile_image(request):
    # Get the user's profile or create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)
    if profile.profile_picture:
        profile_picture_url = request.build_absolute_uri(
            profile.profile_picture.url)

    if request.method == 'POST':
        form = Profile_pictureForm(
            request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Update user first name and last name
            form.save()  # Save profile data
            messages.success(
                request, 'Your profile picture has been updated successfully!')
            log_action(request.user, ADDITION, f"Added profile_picture for {
                request.user.username}", profile)

            # Redirect to a profile view or another page
            return redirect('profile')
    else:
        messages.error(
            request, 'Can not update your profile picture!')

        log_action(request.user, ADDITION, f"Try adding profile_picture for {
            request.user.username}", profile)
        form = ProfileForm(instance=profile)

    context = {'form': form, 'created': created, 'iurl': profile_picture_url}

    return render(request, 'profiles/profile.html', context)

# Delete Profile Picture


@login_required
@permissions_required("users.delete_profile", "users.change_profile")
def delete_profile_image(request):
    # Get or create the user's profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if profile.profile_picture:
            profile.profile_picture.delete()  # Delete the file from storage
            profile.profile_picture = None     # Clear the field
            profile.save()                     # Save the changes

            messages.success(
                request, 'Your profile picture has been deleted successfully!')
            log_action(request.user, DELETION, f"Deleted profile_picture for {
                       request.user.username}", profile)

            return redirect('profile')  # Redirect to the profile view
        else:
            messages.error(request, 'No profile picture to delete.')

    # Redirect in case of a GET request or other methods
    return redirect('profile')


@login_required
@permissions_required("users.view_profile")
def user_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        log_action(request.user, ADDITION, f"Attempted to view/edit profile for {
                   request.user.username}, but no profile exists.")
        profile = Profile(user=request.user)
        profile.save()

    if request.method == 'POST':
        form = ProfileFormLite(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            log_action(request.user, CHANGE, f"Updated profile for {
                       request.user.username}", profile)
            messages.success(request, "Profile updated successfully!")
            return redirect('user_profile')
    else:
        form = ProfileFormLite(instance=profile)
        messages.error(request, "Profile updated unsuccessfully!")

    profile_picture_url = request.build_absolute_uri(
        profile.profile_picture.url) if profile.profile_picture else ""

    if request.method == 'GET':
        log_action(request.user, ADDITION, f"Viewed profile for {
                   request.user.username}", profile)

    context = {
        'profile': profile,
        'form': form,
        'iurl': profile_picture_url
    }

    return render(request, 'profiles/profile.html', context)
