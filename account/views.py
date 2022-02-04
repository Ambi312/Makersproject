from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from oursite.models import Post
from .forms import RegisterForm


class RegisterView(CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')


# class ProfileView(DetailView):
#     model = User
#     template_name = 'registration/profile.html'
def profile(request):
    return render(request, 'registration/profile.html')


class SingInView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')

@ login_required
def favourite_add(request, id):
    post = get_object_or_404(Post, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@ login_required
def favourite_list(request):
    new = Post.objects.filter(favourites=request.user)
    return render(request, 'registration/favourites.html', {'new': new})
