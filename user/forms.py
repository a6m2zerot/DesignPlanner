from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль'}))
    class Meta:
        model = User
        fields = ['username', 'password']

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите логин'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Введите email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Повторите пароль'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

