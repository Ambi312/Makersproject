from django import forms

from .models import User


class RegisterForm(forms.ModelForm):
    image = forms.ImageField()
    password = forms.CharField(max_length=8,
                               required=True,
                               widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=8, required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name', 'password', 'password_confirmation', 'image')

    def clean(self):
        data = self.cleaned_data
        password = data.get('password')
        password_conf = data.pop('password_confirmation')
        if password != password_conf:
            raise forms.ValidationError('Passwords do not match')
        return data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with such email already exists')
        return email

    def save(self, commit=True):
        user = User.objects.create_user(**self.cleaned_data)
        return user


