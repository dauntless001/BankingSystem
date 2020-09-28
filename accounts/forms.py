from django import forms
from django.contrib.auth import get_user_model
from .models import User, Account


class LoginForm(forms.Form):
    username = forms.CharField(max_length=15, widget=forms.TextInput)
    password = forms.CharField(max_length=15, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=40, widget=forms.TextInput)
    last_name = forms.CharField(max_length=40, widget=forms.TextInput)
    username = forms.CharField(max_length=40, widget=forms.TextInput)
    email = forms.EmailField(max_length=40, widget=forms.EmailInput)
    password = forms.CharField(max_length=40, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=40, widget=forms.PasswordInput)

    def clean_data(self):
        data = self.clean_data
        return data
    
    def get_username(self):
        User = get_user_model
        user = self.clean_data.get('username')
        username = User.objects.get(username=user)
        if username.exists:
            raise forms.ValidationError('Username Taken Bruv')
    
    def get_password(self):
        password = self.clean_data.get('password')
        password2 = self.clean_data.get('password2')
        if (password or password2 == '') or (password != password2):
            raise forms.ValidationError('Password error, try again')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['image', 'gender']


class AccountForm(forms.Form):
    account_number = forms.IntegerField()

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)
