from django import forms
from .models import *


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('user', 'likes',)


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'likes')


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'post')


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Image
        fields = ('image', )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('post', 'body')
        exclude = ('post',)
