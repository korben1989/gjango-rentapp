from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.validators import RegexValidator
from django.forms import models
from .models import Property, PropertyImages, PropertyInfo, PropertyAddress, PropertyAmenities, PropertyAddUnit
from crispy_forms.helper import FormHelper


User = get_user_model()
class RegisterUserForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField(
        validators=[RegexValidator(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$',
        message='Put a valid email adress!')],
        required=True
    )
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


class PropertyForm(models.ModelForm):
    # images = forms.ImageField(required=True,
    #                           widget=forms.FileInput(attrs={'allow_multiple_selected': True}))
    class Meta:
        model = Property
        fields = ('title', 'property_description', 'price', 'phone')

        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Phone number',
                                            'data-mask':'(000) 000-0000'}),
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Please enter a name',}
                                            # 'style': 'text-transform: capitalize'}
                                     ),
            'price': forms.NumberInput(attrs={'class': 'form-control',
                                            'placeholder': 'Monthly rent', }),
            'property_description': forms.Textarea(attrs={'class': 'form-control',
                                            'placeholder': 'Write several sentences describing '
                                                           'the upgrades and desirable features '
                                                           'that will attract renters to your property.',
                                                 'rows': 5})
        }

    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for k, v in self.fields.items():
            if 'placeholder' in v.widget.attrs:
                continue
            else:
                v.widget.attrs['placeholder'] = k.capitalize()


class ProperyAddressForm(models.ModelForm):
    class Meta:
        model = PropertyAddress
        fields = ('address', 'neighborhood', 'area', 'city', 'state', 'postcode')


class PropertyAmenitiesForm(models.ModelForm):
    class Meta:
        model = PropertyAmenities
        fields = ('appliances', 'floor_covering', 'cooling_type', 'heating_type', 'rooms',
                  'outdoor_amenities', 'parking', 'view')


class PropertyInfoForm(models.ModelForm):
    class Meta:
        model = PropertyInfo
        fields = ('property_type', 'bedrooms', 'bathrooms', 'square_footage', 'HOA_dues',
                  'lease_terms')

        widgets = {
            'square_footage': forms.NumberInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Square footage'}),
            'HOA_dues': forms.NumberInput(attrs={'class': 'form-control',
                                                     'placeholder': 'HOA dues'}),
            'lease_terms': forms.Textarea(attrs={'class': 'form-control',
                                                     'placeholder': 'Describe lease terms: Owner pays for water. '
                                                                    'Renter is responsible for gas '
                                                                    'and electric. No smoking allowed.',
                                                 'rows': 5})
        }

    def __init__(self, *args, **kwargs):
        super(PropertyInfoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class PropertyImagesForm(models.ModelForm):
    class Meta:
        model = PropertyImages
        fields = ('images', )
        widgets = {
            'images': forms.FileInput(attrs={'class': 'form-control',
                                                     'allow_multiple_selected': True})
        }

    def __init__(self, *args, **kwargs):
        super(PropertyImagesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class PropertyAddUnitForm(models.ModelForm):
    class Meta:
        model = PropertyAddUnit
        fields = ['title_unit', 'bedrooms_unit', 'bathrooms_unit',
                  'square_footage_unit', 'price_unit', 'image_unit']

class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for k, v in self.fields.items():
            if k == 'username':
                v.widget.attrs['placeholder'] = 'Email'
            else:
                v.widget.attrs['placeholder'] = k.capitalize()