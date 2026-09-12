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



