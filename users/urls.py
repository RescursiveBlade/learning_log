"""定义 users 的 URL 模式"""
from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register'),
    # 包含默认的认证 URL（登录、注销、密码修改等）
    path('', include('django.contrib.auth.urls')),
]