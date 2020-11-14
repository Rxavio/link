from django import forms
from .models import Profile,Booking, Contact
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm#
from django.contrib.auth import authenticate



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio','gender', 'address', 'age', 'telephone', 'nationalid','image','image2','image3')
 

# class CreateUserForm(UserCreationForm):
#     email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')
    
    
# 	class Meta:
# 		model = User
# 		fields = ['username', 'email', 'password1', 'password2']   
  
class CreateUserForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')
 
 

	class Meta:
		model = User
		fields = ('email', 'username', 'password1', 'password2', )  
  
  
	def clean_email(self):
			email = self.cleaned_data['email'].lower()
			try:
				user = User.objects.exclude(pk=self.instance.pk).get(email=email)
			except User.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" is already exist.' % email)
  
  
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username','email']  
 
 
class AvailabilityForm(forms.Form):
    check_in = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])
    check_out = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])
          
class ContactForm(ModelForm):
	class Meta:
		model = Contact
		fields = '__all__'          
          