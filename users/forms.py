from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, ProhibitNullCharactersValidator, validate_image_file_extension
from .validators import NoFutureDateValidator


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, validators=[MaxLengthValidator(64)])
    password = forms.CharField(max_length=256, validators=[MaxLengthValidator(256)], widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.Form):  # Fulfils req for 4 field form (picture, date, description, public)
    # profile_picture = forms.ImageField(required=False, label='Profile Picture', validators=[validate_image_file_extension])
    description = forms.CharField(widget=forms.Textarea, required=False, validators=[ProhibitNullCharactersValidator(),
                                                                                     MaxLengthValidator(5000)])
    public = forms.BooleanField(required=False)
    DateOfBirth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}),
                                  validators=[NoFutureDateValidator()],
                                  label='Date of Birth')
    webpage = forms.URLField(required=False, widget=forms.URLInput(), max_length=500, label='Your Own Website',
                             validators=[ProhibitNullCharactersValidator(), MaxLengthValidator(500)])
