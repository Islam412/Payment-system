from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 450px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;', 'id': "", 'placeholder':'Username'}), max_length=100, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 450px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;' , 'id': "", 'placeholder':'Email Address'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 450px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;', 'id': "", 'placeholder':'Password'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 450px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;', 'id': "", 'placeholder':'Confirm Password'}), required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']