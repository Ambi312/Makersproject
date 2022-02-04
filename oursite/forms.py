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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class UserPostRelationForm(forms.ModelForm):
    class Meta:
        model = UserPostRelation
        fields = ('post', 'like', 'favorites')

