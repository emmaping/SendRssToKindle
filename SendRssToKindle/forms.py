from django import forms
from django.contrib.auth.models import User
from models import KindleUser

class UserForm(forms.Form):
    username = forms.CharField()
    kindleemail = forms.EmailField(required=False)
    scheduletime = forms.TimeField(required=False)
    
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password1= forms.CharField(min_length = 6,max_length=10, widget=forms.PasswordInput(), label = 'Password')
    password2= forms.CharField(min_length = 6,max_length=10, widget=forms.PasswordInput(), label = 'Password again')
    kindleemail = forms.EmailField(required=False, label = 'Binded Kindle mail')
    scheduletime = forms.TimeField(required=False, label = 'Scheduled deliver time')
    
    def clean_username(self): # check if username does not exist before
        try:
            User.objects.get(username=self.cleaned_data['username']) #get user from user model
        except User.DoesNotExist :
            return self.cleaned_data['username']
        raise forms.ValidationError("this user exist already")


    def clean(self): # check if password 1 and password2 match each other
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:#check if both pass first validation
            if self.cleaned_data['password1'] != self.cleaned_data['password2']: # check if they match each other
                raise forms.ValidationError("passwords do not match each other")
    
        return self.cleaned_data
    
    
    def save(self): # create new user
        newuser=User.objects.create_user(self.cleaned_data['username'],
                                  self.cleaned_data['email'],
                                  self.cleaned_data['password1'])
        kindleuser = KindleUser()
        kindleuser.user = newuser
        kindleuser.kindleemail = self.cleaned_data['kindleemail']
        kindleuser.scheduletime = self.cleaned_data['scheduletime']
        kindleuser.save()
        return kindleuser
    
