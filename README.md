🚀 My Django Learning Journey (我的 Django 学习之旅)
Recursive thinking, sharp focus. Documenting my journey from zero to hero.
递归之刃，劈开技术迷雾。记录从零开始的极客修行。

This document records my first two days of learning Django (based on Python Crash Course Chapter 18). It covers everything from setting up the environment to building a complete multi-page web application.
本文记录了我学习 Django 前两天的历程（基于《Python编程：从入门到实践》第18章）。涵盖了从零搭建环境到完成多页面 Web 应用的全过程。

📅 Day 1: Environment Setup & Core Concepts (第一天：环境搭建与核心概念)
1. Setting Up the Virtual Environment (搭建虚拟环境)
To isolate my project dependencies, I created a virtual environment:
为了隔离项目依赖，我创建了一个虚拟环境：

cmd
cd C:\Users\ooo\learning_log
python -m venv ll_env
ll_env\Scripts\activate  # Windows
Note: The terminal prefix (ll_env) indicates the environment is active.
注意：终端前缀显示 (ll_env) 表示环境已激活。

2. Installing Django & Creating the Project (安装 Django 并创建项目)
cmd
pip install --upgrade pip
pip install django
django-admin startproject ll_project .
⚠️ Pitfall: Do not forget the dot (.) at the end of the startproject command! It creates the project in the current directory, making deployment much easier later.
⚠️ 踩坑：千万别忘了 startproject 命令末尾的句点 (.)！它表示在当前目录创建项目，方便以后部署。

3. Creating the App & Defining Models (创建应用与定义模型)
cmd
python manage.py startapp learning_logs
In learning_logs/models.py, I defined two models: Topic and Entry (a one-to-many relationship).
在 models.py 中，我定义了两个模型：Topic 和 Entry（多对一关系）。

python
from django.db import models

class Topic(models.Model):
    """A topic the user is learning about. (用户学习的主题)"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Entry(models.Model):
    """Something specific learned about a topic. (学到的具体知识)"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return f"{self.text[:50]}..."
Registering the models in admin.py (在 admin.py 中注册模型):

python
from django.contrib import admin
from .models import Topic, Entry

admin.site.register(Topic)
admin.site.register(Entry)
4. Database Migration & Superuser (数据库迁移与超级管理员)
cmd
python manage.py makemigrations learning_logs
python manage.py migrate
python manage.py createsuperuser
Pitfall: When setting the superuser password, the terminal shows no characters (no asterisks). This is a normal security feature.
踩坑：设置超级管理员密码时，终端不显示任何字符（没有星号）。这是正常的安全机制。

5. Testing with Django Shell (使用 Django Shell 测试)
cmd
python manage.py shell
python
from learning_logs.models import Topic
Topic.objects.all()
t = Topic.objects.get(id=1)
t.entry_set.all()  # Reverse lookup via ForeignKey (通过外键反向查询)
exit()
📅 Day 2: Multi-page Web App, MTV Pattern & Debugging (第二天：多页面开发、MTV模式与排错)
1. Building the "MTV" Skeleton (搭建 MTV 骨架)
I learned that Django separates data (Model), logic (View), and appearance (Template).
我学到了 Django 将数据(Model)、逻辑(View)和外观(Template)分离开来。

Step 1: URLs (URL 路由)

ll_project/urls.py (Project level - 项目级):

python
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('learning_logs.urls')),
]
learning_logs/urls.py (App level - Created this file - 应用级，新建此文件):

python
from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'), # Dynamic ID capture (捕获动态ID)
]
Step 2: Views (视图 - 逻辑与取数据)
In learning_logs/views.py:

python
from django.shortcuts import render
from .models import Topic, Entry

def index(request):
    return render(request, 'learning_logs/index.html')

def topics(request):
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added') # Descending order (降序)
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)
Step 3: Templates (模板 - 继承与展示)
Critical structure path: learning_logs/templates/learning_logs/
关键路径结构：learning_logs/templates/learning_logs/

Base Template (base.html - 基础模板):

html
<p>
    <a href="{% url 'learning_logs:index' %}">Learning Log</a> -
    <a href="{% url 'learning_logs:topics' %}">Topics</a>
</p>
{% block content %}{% endblock content %}
Topics List (topics.html - 主题列表页):

html
{% extends 'learning_logs/base.html' %}
{% block content %}
  <ul>
    {% for topic in topics %}
      <li><a href="{% url 'learning_logs:topic' topic.id %}">{{ topic.text }}</a></li>
    {% empty %}
      <li>No topics have been added yet. (暂未添加主题)</li>
    {% endfor %}
  </ul>
{% endblock content %}
Topic Detail (topic.html - 主题详情页):

html
{% extends 'learning_logs/base.html' %}
{% block content %}
  <p>Topic: {{ topic.text }}</p>
  {% for entry in entries %}
    <p>{{ entry.date_added|date:'M d, Y H:i' }}</p>
    <p>{{ entry.text|linebreaks }}</p>
  {% empty %}
    <p>There are no entries for this topic yet. (此主题暂无条目)</p>
  {% endfor %}
{% endblock content %}
2. Debugging Log (Hard-earned Lessons / 血泪排错日志)
TemplateDoesNotExist: The HTML file was missing or in the wrong folder. Django requires an exact nested path: app_name/templates/app_name/file.html.

模板找不到：HTML文件缺失或放错位置。路径必须是严格的双层嵌套。

NoReverseMatch: Reverse for 'topic' not found: The HTML used {% url 'learning_logs:topic' %}, but the urls.py didn't have a route named 'topic'. Fixed by adding the path.

路由反查失败：HTML里用了 {% url %}，但 urls.py 里没写对应的 name='topic'。补全路由即可。

AttributeError: module 'learning_logs.views' has no attribute 'topic': The urls.py pointed to a view function that hadn't been written yet. Fixed by adding def topic(request, topic_id): ....

属性错误：路由指向了 views.topic 函数，但视图里还没写。在 views.py 补全函数即可。

FieldError: Cannot resolve keyword 'date_added' into field. Choices are: data_added: Typo in models.py (data_added instead of date_added). Fixed by correcting the spelling and resetting the database (deleted db.sqlite3 and migrations, then re-ran makemigrations and migrate).

字段错误：拼写错误（把日期 date 拼成了数据 data）。改对拼写后，删除 db.sqlite3 和 migrations 文件，重新迁移重建数据库。

3. Git & GitHub Workflow (Git 与 GitHub 工作流)
cmd
git rm --cached db.sqlite3  # Stop tracking the local database (停止跟踪本地数据库)
git commit -m "Remove db.sqlite3 from tracking"
git push
Note: Local databases and virtual environments should never be pushed to GitHub. Always use a .gitignore file.
注意：本地数据库和虚拟环境永远不应该被推送到 GitHub。务必使用 .gitignore 文件。

🎯 Upcoming Goals (未来计划 - Chapter 18.5)
□ Implement User Registration, Login, and Logout. (实现用户注册、登录与注销)
□ Use @login_required to restrict access. (使用装饰器限制未登录访问)
□ Ensure users can only see and edit their own notes. (确保用户只能看到并编辑自己的笔记)
□ Deploy the application to a production server. (将应用部署到生产服务器)
"True recursion is calling a better version of yourself every day, until you hit the base case."
“所谓递归，就是每天调用一次更优秀的自己，直到达到基案。”

📅 Day 3: User Accounts & Authentication (第三天：用户账户与身份验证)

1. Core Progress (核心进展)
Today, I implemented the core user authentication system for my "Learning Log" app. I created a new users app and integrated Django's built-in authentication framework.
今天，我为“学习笔记”应用实现了核心的用户认证系统。我创建了一个新的 users 应用，并集成了 Django 内置的认证框架。

User Registration: Implemented a form for users to create their own accounts.

用户注册：实现了用户创建自己账号的表单。

User Login/Logout: Configured templates and URL routing for logging in and out.

用户登录/注销：配置了登录和注销的模板与路由。

Dynamic Navigation: Updated base.html to show different links based on authentication status.

动态导航栏：更新了 base.html，根据用户登录状态动态显示链接。

2. Key Code & Line-by-Line Explanations (关键代码与逐行解释)
2.1 User Registration Form (users/forms.py)
I used Django's UserCreationForm to avoid writing password validation and encryption logic from scratch.
我使用了 Django 内置的 UserCreationForm，避免从零编写密码验证和加密逻辑。

python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='请输入有效的邮箱地址。')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
Line-by-line Explanation (逐行解释):

UserCreationForm automatically handles password hashing (encryption) and password strength validation.

UserCreationForm 自动处理密码哈希（加密）和密码强度验证。

email = forms.EmailField(...) adds an email field to the default registration form.

添加了一个邮箱字段到默认的注册表单中。

class Meta defines which fields the form will render on the HTML page.

定义了表单会在 HTML 页面上渲染哪些字段。

2.2 Registration View (users/views.py)
This view handles both displaying the blank form (GET) and processing submitted data (POST).
这个视图同时处理“显示空表单（GET）”和“处理提交的数据（POST）”。

python
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def register(request):
    """注册新用户"""
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user) # Automatically log in after registration (自动登录)
            return redirect('learning_logs:index')

    context = {'form': form}
    return render(request, 'registration/register.html', context)
Line-by-line Explanation (逐行解释):

if request.method != 'POST': checks if it's a GET request (user first visiting the page).

检查是否是 GET 请求（用户第一次访问页面）。

form.save() saves the new user to the database (Django handles the encryption).

将新用户保存到数据库（Django 自动处理加密）。

login(request, new_user) logs the user in immediately after registration, preventing them from having to re-enter their credentials.

注册后立即让用户登录，避免他们重新输入账号密码。

2.3 URLs (users/urls.py)
python
from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')), # Built-in login/logout (内置的登录/注销)
]
3. Debugging Log: The "Ghost" Errors (踩坑日志：幽灵报错)
This section is the most valuable part of my learning today. I hit several classic Django/Windows traps.
这一节是我今天学习中最重要的部分。我踩中了几个经典的 Django 与 Windows 陷阱。

Trap 1: TemplateDoesNotExist (registration/login.html)

Reason: Django's built-in auth system strictly requires login templates to be inside a registration/ folder, not a users/ folder.

原因：Django 内置的认证系统严格规定，登录模板必须放在 registration/ 文件夹下，而不是 users/ 文件夹下。

Solution: Create users/templates/registration/login.html.

解决：创建了 users/templates/registration/login.html。

Trap 2: HTTP ERROR 405 (Logout Failed)

Reason: Django 6.1.1 no longer allows logging out via a simple GET request (a standard <a> link). It requires a POST request for security.

原因：Django 6.1.1 不再允许通过简单的 GET 请求（普通的 <a> 链接）注销。出于安全考虑，它要求使用 POST 请求。

Solution: Replaced the <a> link in base.html with a <form method="post"> containing {% csrf_token %}.

解决：将 base.html 中的 <a> 链接替换为包含 {% csrf_token %} 的 <form method="post">。

Trap 3: The "Ghost" Blank Page (幽灵空白页)

Reason: The page only showed the navigation bar but no content. This happens when {% block content %} is missing in base.html, or when the child template is not saved to the disk.

原因：页面只显示导航栏，没有任何内容。这通常是因为 base.html 中缺少 {% block content %}，或者子模板没有保存到硬盘上。

Solution: Ensure base.html ends with {% block content %}{% endblock content %}. Always hit Ctrl+S and use Ctrl+Shift+N (Incognito) to clear browser cache.

解决：确保 base.html 以 {% block content %}{% endblock content %} 结尾。务必按 Ctrl+S 保存，并使用 Ctrl+Shift+N（无痕模式）清除浏览器缓存。

Trap 4: Windows File Naming Traps (Windows 文件名陷阱)

Reason: I named a file new.entry.html (dot) instead of new_entry.html (underscore). Windows also hides file extensions (.txt), making me think the file was .html.

原因：我把文件命名成了 new.entry.html（点号），而不是 new_entry.html（下划线）。Windows 也隐藏了文件扩展名（.txt），让我误以为文件是 .html。

Solution: Always double-check file names in File Explorer with "File name extensions" turned on.

解决：始终在文件资源管理器中开启“文件扩展名”，仔细检查文件名。

4. Reflection (今日反思)
Today was incredibly frustrating but extremely rewarding. I encountered "ghost" errors, HTTP 405 errors, and Windows file naming traps. I learned that 80% of development is troubleshooting, not writing code. I am no longer just copying code; I am learning how to diagnose the environment, understand Django's underlying conventions, and solve problems systematically.
今天非常折磨，但也极有收获。我遇到了“幽灵”报错、HTTP 405 错误和 Windows 文件名陷阱。我学到了开发中 80% 的时间是在排查问题，而不是写代码。我不再只是复制粘贴代码，而是在学习如何诊断环境、理解 Django 底层的约定，并系统地解决问题。

Next Step: User Data Isolation (Restrict users to only see their own data).
下一步：用户数据隔离（限制用户只能看到自己的数据）。






