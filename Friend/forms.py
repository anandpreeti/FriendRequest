from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from .models import User, Friend_Request
from django import forms

class UserCreateForm(UserCreationForm):

	class Meta(UserCreationForm):
		model = User
		fields = ('username', 'password1', 'password2')

class FriendRequestCreateForm(forms.ModelForm):

	class Meta:
		model = Friend_Request
		fields = ("__all__")
