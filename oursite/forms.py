from django import forms
from .models import *


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('user', 'likes',)


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user',)


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)
