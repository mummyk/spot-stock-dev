from django import forms
from .models import AppLabel, UserProducts


class UserProfileForm(forms.ModelForm):
    app_labels = forms.ChoiceField(
        choices=AppLabel.get_choices(), widget=forms.SelectMultiple)

    class Meta:
        model = UserProducts  # Assuming this is your model
        fields = ['app_labels']  # Add other fields as necessary
