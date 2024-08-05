from typing import Any
from django import forms
from .models import Contestant, Pageant, ContactUs, UserFeedBack, RegistrationStatus

class ContestantForm(forms.ModelForm):
    class Meta:
        model = Contestant
        fields = '__all__'
        exclude = ['approved']


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'


class RegistrationStatusForm(forms.ModelForm):
    class Meta:
        model = RegistrationStatus
        fields = ['is_registration_open']

class UserFeedBackForm(forms.ModelForm):
    class Meta:
        model = UserFeedBack
        fields = ['name', 'email', 'feedback']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        feedback = cleaned_data.get('feedback')

        if not name or not email or not feedback:
            raise forms.ValidationError('All fields are required.')