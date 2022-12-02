from wsgiref.handlers import format_date_time
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.core.exceptions import ValidationError
from datetime import date

class UserRegisterForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'input100',
                'type': 'text',
                'name': 'username',
                'placeholder': 'Username'
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'input100',
                'type': 'email',
                'name': 'email',
                'placeholder': 'Email'
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'input100',
                'type': 'password',
                'name': 'password1',
                'placeholder': 'Password'
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'input100',
                'type': 'password',
                'name': 'password2',
                'placeholder': 'Confirm Password'
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("The email entered is already registered.")
       return email

class CustomerRegisterForm(forms.ModelForm):

    dni = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'input100',
                'type': 'number',
                'name': 'dni',
                'placeholder': 'DNI'
            }
        )
    )

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'input100',
                'type': 'text',
                'name': 'name',
                'placeholder': 'Name'
            }
        )
    )

    surname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'input100',
                'type': 'text',
                'name': 'surname',
                'placeholder': 'Surname'
            }
        )
    )

    date_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'input100',
                'type': 'text',
                'name': 'date_birth',
                'placeholder': 'Birthdate',
                'onfocus': "(this.type = 'date')"
            }
        )
    )

    gender = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'input100',
                'name': 'gender',
                'placeholder': 'Gender',
            }
        ),
        choices=GENDER_PERSON_CHOICES,
    )

    cellphone_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'input100',
                'type': 'number',
                'name': 'cellphone_number',
                'placeholder': 'Cellphone Number'
            }
        )
    )

    literary_prefer = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'input100',
                'name': 'literary_prefer',
                'placeholder': 'Literary Prefer',
            }
        ),
        choices=GENDER_CHOICES,
    )

    class Meta:
        model = Customer
        fields = ['dni', 
                'name', 
                'surname', 
                'date_birth', 
                'gender',
                'cellphone_number',
                'literary_prefer',
                'country',
                'region',
                'city',
                ]

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if (dni<100000) or (dni>10000000000):
                raise ValidationError("The entered ID is not valid.")
        if Customer.objects.filter(dni=dni).exists():
            raise ValidationError("The entered ID is already registered.")
        return dni
    
    def clean_date_birth(self):
        dob = self.cleaned_data.get('date_birth')
        age = (date.today() - dob).days / 365
        if age < 18:
            raise ValidationError('You must be at least 18 years old')
        return dob

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'input100',
                'type': 'text',
                'name': 'username',
                'placeholder': 'Username'
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'input100',
                'type': 'email',
                'name': 'email',
                'placeholder': 'Email'
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'email']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("The email entered is already registered.")
        return email

class CustomerUpdateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'input100',
                'type': 'text',
                'name': 'name',
                'placeholder': 'Name'
            }
        )
    )

    surname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'input100',
                'type': 'text',
                'name': 'surname',
                'placeholder': 'Surname'
            }
        )
    )

    date_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'input100',
                'type': 'text',
                'name': 'date_birth',
                'placeholder': 'Birthdate',
                'onfocus': "(this.type = 'date')"
            }
        )
    )

    gender = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'input100',
                'name': 'gender',
                'placeholder': 'Gender',
            }
        ),
        choices=GENDER_PERSON_CHOICES,
    )

    cellphone_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'input100',
                'type': 'number',
                'name': 'cellphone_number',
                'placeholder': 'Cellphone Number'
            }
        )
    )

    literary_prefer = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'input100',
                'name': 'literary_prefer',
                'placeholder': 'Literary Prefer',
            }
        ),
        choices=GENDER_CHOICES,
    )

    class Meta:
        model = Customer
        fields = ['name', 'surname', 'date_birth',
                  'gender', 'cellphone_number', 'literary_prefer']
    
    def clean_date_birth(self):
        dob = self.cleaned_data.get('date_birth')
        age = (date.today() - dob).days / 365
        if age < 18:
            raise ValidationError('You must be at least 18 years old.')
        return dob

class AddCardForm(forms.ModelForm):

    type_card = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'input100',
                'name': 'type_card',
                'placeholder': 'Type Card',
            }
        ),
        choices=TYPE_CARD,
    )

    number_card = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'input100',
                'type': 'number',
                'name': 'number_card',
                'placeholder': 'Number Card',
            }
        )
    )

    cvv = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'input100',
                'type': 'number',
                'name': 'number_card',
                'placeholder': 'CVV'
            }
        )
    )

    cardholder = forms.RegexField(regex=r'[a-zA-Z_. -]+$',
        widget=forms.TextInput(
            attrs={
                'class': 'input100',
                'type': 'text',
                'name': 'cardholder',
                'placeholder': 'Cardholder'
            }
        )
    )

    expiration_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'input100',
                'type': 'text',
                'name': 'expiration_date',
                'placeholder': 'Expiration Date',
                'onfocus': "(this.type = 'date')"
            }
        )
    )

    class Meta:
        model = PaymentMethod
        fields = [
            'type_card',
            'number_card',
            'cvv',
            'cardholder',
            'expiration_date'
        ]

    def clean_number_card(self):
        number_card = self.cleaned_data.get('number_card')
        if len(str(number_card)) != 16 or (not str(number_card).isdigit()):
            raise ValidationError("Please enter a valid card number.")
        if PaymentMethod.objects.filter(number_card=number_card).exists():
            raise ValidationError("This card is already registered.")
        return number_card
    
    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        if len(str(cvv)) != 3 or (not str(cvv).isdigit()):
            raise ValidationError("Please enter a valid CVV.")
        return cvv

    def clean_expiration_date(self):
        dob = self.cleaned_data.get('expiration_date')
        days = (dob - date.today()).days
        print(days)
        if days <= 0:
            raise ValidationError('Select a valid date.')
        return dob

class AddressShippingForm(forms.ModelForm):

    address_shipping = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'text',
                'name': 'address_shipping',
                'placeholder': 'Address Shipping'
            }
        )
    )

    class Meta:
        model = Shipping
        fields = [
            'country',
            'region',
            'city',
            'address_shipping',
        ]

class ReturnOrderForm(forms.ModelForm):

    cause = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'name': 'cause',
                'placeholder': 'Cause',
            }
        ),
        choices=CAUSE_RETURN_CHOICES,
    )

    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'text',
                'name': 'description',
                'placeholder': 'Description'
            }
        )
    )
    class Meta:
        model = ReturnOrder
        fields = [
            'cause',
            'description',
        ]

class PickUpForm(forms.ModelForm):

    class Meta:
        model = PickUpStore
        fields = [
            'branch_office_pickup'
        ]