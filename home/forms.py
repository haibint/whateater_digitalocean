from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
        
        #For some reason, if you put "forms.Form" instead of "forms.ModelForm", the html generation will go wrong
class UserSignInForm(forms.Form):
    username = forms.CharField
    password = forms.CharField(widget=forms.PasswordInput)
    