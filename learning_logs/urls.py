"""定义 learning_logs 的 URL 模式"""
from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    path('', views.index, name='index'),
]