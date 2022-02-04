from datetime import datetime
from django import forms
from .models import *


class CreatePostForm(forms.ModelForm):
    created = forms.DateTimeField(initial=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), required=False)

    class Meta:
        model = Post
        exclude = ('user',)

    # def save(self, commit=True):
    #     user = self.request.user
    #     post = Post.objects.create(**self.cleaned_data)
    #     post.user = user
    #     return post

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
