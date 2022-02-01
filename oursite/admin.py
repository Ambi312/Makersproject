from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Comment)


class ImageInLineAdmin(admin.TabularInline):
    model = Image
    fields = ('image',)
    max_num = 20

