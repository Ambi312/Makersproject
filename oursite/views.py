from django.shortcuts import render
from .models import Author


def index(request):
    return render(request, 'index.html')


def posts_list(request, slug):
    posts = Author.objects.filter(category__slug=slug)
    return render(request, 'oursite/list.html', locals())

