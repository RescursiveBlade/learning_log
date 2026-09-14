from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def register(request):
    """注册新用户"""
    if request.method != 'POST':
        # 如果是第一次访问，显示空表单
        form = RegisterForm()
    else:
        # 如果是提交表单，处理数据
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            # 保存用户到数据库
            new_user = form.save()
            # 注册成功后，自动让该用户登录（这是业界惯例，体验更好）
            login(request, new_user)
            # 登录后跳转到主页
            return redirect('learning_logs:index')

    # 将表单发送给模板
    context = {'form': form}
    return render(request, 'registration/register.html', context)