from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic          # 基于 Topic 模型创建表单
        fields = ['text']      # 表单中只包含 text 字段
        labels = {'text': ''}  # 告诉 Django 不要为 text 字段生成标签（显示更简洁）
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}  # 指定 text 字段使用 Textarea 小部件，并设置列数为 80
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry          # 基于 Entry 模型创建表单
        fields = ['text']      # 表单中只包含 text 字段
        labels = {'text': ''}  # 告诉 Django 不要为 text 字段生成标签（显示更简洁）
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}  # 指定 text 字段使用 Textarea 小部件，并设置列数为 80