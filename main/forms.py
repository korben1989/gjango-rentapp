from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import models
from .models import AddPropertyGoogle
from crispy_forms.helper import FormHelper


User = get_user_model()
class RegisterUserForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for k, v in self.fields.items():
            v.widget.attrs['placeholder'] = k.capitalize()


class AddPropertyGoogleForm(models.ModelForm):
    class Meta:
        model = AddPropertyGoogle
        fields = ('location', 'apartment_unit',
                  'property_type', 'city', 'state', 'postal_code', 'country')

    def __init__(self, *args, **kwargs):
        super(AddPropertyGoogleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for k, v in self.fields.items():
            v.widget.attrs['placeholder'] = k.capitalize()


class LoginUserForm(AuthenticationForm):
    email = forms.EmailField
    password = forms.PasswordInput

    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for k, v in self.fields.items():
            if k == 'username':
                v.widget.attrs['placeholder'] = 'Email'
            else:
                v.widget.attrs['placeholder'] = k.capitalize()

