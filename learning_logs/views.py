from django.shortcuts import render
from .models import Topic, Entry  # <--- 新增导入
from .forms import TopicForm  # <--- 新增导入

def index(request):
    """学习笔记的主页"""
    return render(request, 'learning_logs/index.html')

def topics(request):  # <--- 新增函数
    """显示所有的主题"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    """允许用户创建新主题"""
    if request.method != 'POST':
        # 创建一个空的表单
        form = TopicForm()
    else:
        # 提交了数据，对其进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
