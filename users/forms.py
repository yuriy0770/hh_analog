from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUsers


class UserForm(UserCreationForm):
    phone = forms.CharField(max_length=50, required=False, label='Телефон')

    class Meta:
        model = CustomUsers
        fields = ['username', 'email', 'phone', 'user_type', 'password1', 'password2']
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'user_type': 'Вы кто?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})