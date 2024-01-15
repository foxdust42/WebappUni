from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator


class NewPostForm(forms.Form):
    title = forms.CharField(max_length=300, validators=[MaxLengthValidator(300), MinLengthValidator(1)])
    content = forms.CharField(max_length=100000, validators=[MaxLengthValidator(100000), MinLengthValidator(1)],
                              widget=forms.Textarea())


class NewCommentForm(forms.Form):
    content = forms.CharField(max_length=500000, validators=[MaxLengthValidator(5000), MinLengthValidator(1)], widget=forms.Textarea())
