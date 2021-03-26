from django.contrib.auth.forms import UserCreationForm, UserChangeForm, User
from django.forms import ModelForm

from .models import CustomUser, Faculty_Assignment


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateAssignment(ModelForm):
    class Meta:
        model = Faculty_Assignment
        fields = ['marks','description','deadline','PDF']