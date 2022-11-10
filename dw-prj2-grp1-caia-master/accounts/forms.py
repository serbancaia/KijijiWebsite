from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    """
    Form used for visitor sign up
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')


class LoginForm(forms.Form):
    """
    Form used for visitor login
    """
    username = forms.CharField(label="Your username", max_length=100)
    password = forms.CharField(label="Your password", max_length=100)


class AccountForm(UserChangeForm):
    """
    Form used to update a customer's profile
    """
    # Empty image field
    profile_picture = forms.ImageField(required=False)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
