from django.contrib.admin import ModelAdmin

from .models import *
from django.contrib import admin
from .models import Post, Comment


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('name', 'body')


class ImageInLineAdmin(admin.TabularInline):
    model = Image
    fields = ('image',)
    max_num = 20


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInLineAdmin]





