from django import forms
from .models import Booking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BookingForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'placeholder': 'DD/MM/YYYY',
                'type': 'text'
            }
        ),
        input_formats=['%d/%m/%Y']
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'placeholder': 'HH:MM AM/PM',
                'type': 'text'
            }
        ),
        input_formats=['%I:%M %p', '%I:%M%p']
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'placeholder': 'HH:MM AM/PM',
                'type': 'text'
            }
        ),
        input_formats=['%I:%M %p', '%I:%M%p']
    )

    class Meta:
        model = Booking
        fields = ['hall', 'department', 'date',
                  'start_time', 'end_time', 'purpose']

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email',
                  'password1', 'password2']