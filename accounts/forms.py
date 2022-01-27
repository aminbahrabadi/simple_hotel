from django import forms
from django.contrib.auth import password_validation, get_user_model
from django.forms import ValidationError
from .models import Role


User = get_user_model()


class UserCreateForm(forms.Form):
    username = forms.CharField(max_length=155, label='Username')
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(max_length=255, label='First Name')
    last_name = forms.CharField(max_length=255, label='Last Name')
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    role = forms.ModelMultipleChoiceField(queryset=Role.objects.all(), label='Role')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            try:
                password_validation.validate_password(password)
                return password

            except ValidationError:
                raise ValidationError('Password must be strong enough!')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            is_duplicated = User.objects.filter(username=username).exists()

            if is_duplicated:
                raise ValidationError('Username already exists!')

            return username
