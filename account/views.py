from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
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







