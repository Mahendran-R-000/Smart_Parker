from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import ModelForm

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True,widget=forms.TextInput(attrs={'placeholder':'Enter First name','class':'form-control mb-1','id':'firstname'}))
    last_name = forms.CharField(max_length=30, required=True,widget=forms.TextInput(attrs={'placeholder':'Enter Last name','class':'form-control mb-1','id':'lastname'}))
    email = forms.EmailField(max_length=254,required=True,widget=forms.EmailInput(attrs={'placeholder':'Enter Email','class':'form-control mb-1','id':'email'}))
    password1 = forms.CharField(min_length=8, max_length=10, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password', 'class': 'form-control', 'id': 'password'}),)
    password2 = forms.CharField(min_length=8, max_length=10, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Retype Password', 'class': 'form-control', 'id': 'retypepassword'}),)
    class Meta:
        model = Myusers
        fields = ('first_name','last_name','email', 'password1', 'password2')


class EditProfileForm(ModelForm):
    class Meta:
        model = Myusers
        fields = (
                 'email',
                 'first_name',
                 'last_name'
                )
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'inputEmail'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'inputlname'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'inputfname'})
        }

class ProfileForm(ModelForm):
    class Meta:
             model = UserProfile
             fields = ('city',  'phoneNumber', 'image', 'pincode')

             widgets = {
                 'city': forms.EmailInput(attrs={'class': 'form-control', 'id': 'inputCity', 'type': 'text'}),
                 'phoneNumber': forms.TextInput(attrs={'class': 'form-control', 'id': 'inputphoneno'}),
                 'pincode': forms.TextInput(attrs={'class': 'form-control', 'id': 'pincode'}),

             }

class RentRegisterform(ModelForm):

    class Meta:
        model = RentRegister
        fields = ['place_name','address', 'total_transport', 'money_per_hour','latitude','longitude']


class RentImagesform(RentRegisterform): # here we extending rent register form
    #images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    images = forms.FileField(widget=forms.FileInput(attrs={'id': 'file-input'}))

    class Meta(RentRegisterform.Meta):
        fields = RentRegisterform.Meta.fields + ['images',]


class Reportform(ModelForm):
    class Meta:
        model = Report
        fields = ['location', 'title', 'transport_number', 'description']


class ReportImagesform(Reportform): # here we extending rent register form
    images = forms.FileField(widget=forms.FileInput(attrs={'id': 'file-input'}))

    class Meta(Reportform.Meta):
        fields = Reportform.Meta.fields + ['images',]