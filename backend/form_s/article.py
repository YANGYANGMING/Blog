
from django.core.exceptions import ValidationError
from django import forms
from django.forms import fields
from django.forms import widgets

from repository import models


class ArticleForm(forms.Form):
    title = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '文章标题'})
    )
    summary = fields.CharField(
        widget=widgets.Textarea(attrs={'class': 'form-control', 'placeholder': '文章简介', 'rows': '3'})
    )
    content = fields.CharField(
        widget=widgets.Textarea(attrs={'class': 'kind-content'})
    )
    article_type_id = fields.IntegerField(
        widget=widgets.RadioSelect(choices=models.Article.type_choices)
    )
    category_id = fields.ChoiceField(
        choices=[],
        widget=widgets.RadioSelect
    )
    tag = fields.MultipleChoiceField(
        choices=[],
        widget=widgets.CheckboxSelectMultiple
    )

    def __init__(self, request, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        blog_id = request.session['user_info']['blog__nid']
        self.fields['category_id'].choices = models.Article.objects.filter(blog_id=blog_id).values_list('nid', 'title')
        self.fields['tag'].choices = models.Article.objects.filter(blog_id=blog_id).values_list('nid', 'title')
