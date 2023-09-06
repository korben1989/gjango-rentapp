from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import models
from .models import AddPropertyGoogle


User = get_user_model()
class RegisterUserForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AddPropertyGoogleForm(models.ModelForm):
    class Meta:
        model = AddPropertyGoogle
        fields = ('location', 'apartment_unit',
                  'property_type', 'city', 'state', 'postal_code', 'country')


class LoginUserForm(AuthenticationForm):
    email = forms.EmailField
    password = forms.PasswordInput

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(LoginUserForm, self).__init__(*args, **kwargs)
