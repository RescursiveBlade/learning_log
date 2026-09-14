from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    """用于创建新用户的表单"""
    email = forms.EmailField(required=True, help_text='请输入有效的邮箱地址。')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']