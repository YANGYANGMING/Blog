import uuid
import os
import json

from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.db import transaction

from repository import models
from utils.pagination import Pagination
from utils.xss import XSSFilter
from ..auth.auth import check_login
from ..form_s.article import ArticleForm


@check_login
def index(request):
    """
    博主个人首页
    :param request:
    :return:
    """
    return render(request, 'backend_index.html')

@check_login
def base_info(request):
    """
    博主个人信息
    :param request:
    :return:
    """
    return render(request, 'backend_base_info.html')

@check_login
def upload_avatar(request):
    ret = {'status': False, 'data': None, 'message': None}
    if request.method == 'POST':
        file_obj = request.FILES.get('avatar_img')
        if not file_obj:
            pass
        else:
            file_name = str(uuid.uuid4())
            file_path = os.path.join('static/images/avatar', file_name)
            print(file_path)
            with open(file_path, 'wb') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
            ret['status'] = True
            ret['data'] = file_path

    return HttpResponse(json.dumps(ret))

@check_login
def tag(request):
    """
    博主个人标签管理
    :param rquest:
    :return:
    """
    return render(request, 'backend_tag.html')

@check_login
def category(request):
    """
    博主个人分类管理
    :param request:
    :return:
    """
    return render(request, 'backend_category.html')

@check_login
def article(request, *args, **kwargs):
    """
    博主个人文章管理
    :param request:
    :return:
    """
    blog_id = request.session['user_info']['blog__nid']
    condition = {}
    for k, v in kwargs.items():
        if v == '0':
            pass
        else:
            condition[k] = v
    article_type_id = kwargs.get('article_type_id')
    category_id = kwargs.get('category_id')
    category_list = models.Category.objects.filter(blog_id=blog_id).values('nid', 'title')
    type_list = list(map(lambda item: {'nid': item[0], 'title': item[1]}, models.Article.type_choices))

    # if article_type_id == 0:
    #     type_list = map(lambda item: {'nid': item[0], 'title': item[1]}, models.Article.type_choices)
    #     if category_id == 0:
    #         pass
    #     else:
    #         condition['category_id'] = category_id
    # else:
    #     type_obj = models.Article.objects.filter(id=article_type_id).first()
    #     type_list = map(lambda item: {'nid': item[0], 'title': item[1]}, models.Article.type_choices)
    #
    #     vlist = type_obj.article_type_id.all().values_list('nid', 'title')  # [(1,),(2,),(3,)]
    #     if not vlist:
    #         classification_id_list = []
    #     else:
    #         classification_id_list = list(zip(*vlist))[0]
    #
    #     if category_id == 0:
    #             condition['category_id__in'] = classification_id_list
    #     else:
    #         if category_id in classification_id_list:
    #             condition['category_id'] = category_id
    #         else:
    #             #方向指定，分类不在其中  [1,2,3]     分类：5
    #             kwargs['category_id'] = 0
    #             condition['category_id'] = classification_id_list

    condition['blog_id'] = blog_id
    data_count = models.Article.objects.filter(**condition).count()
    page = Pagination(request.GET.get('p', 1), data_count)
    page_str = page.page_str(reverse('article', kwargs=kwargs))
    kwargs['p'] = page.current_page

    result = models.Article.objects.filter(**condition).order_by('-nid').only('nid', 'title', 'blog').select_related(
        'blog')[page.start:page.end]

    return render(request, 'backend_article.html', locals())

@check_login
def add_article(request):
    """
   添加文章
   :param request:
   :return:
   """
    if request.method == 'GET':
        form = ArticleForm(request=request)
        return render(request, 'backend_add_article.html', {'form': form})
    elif request.method == 'POST':
        form = ArticleForm(request=request, data=request.POST)
        if form.is_valid():
            with transaction.atomic():  #在执行上下文里面的内容时候时，遇到错误执行回滚操作，类似mysql回滚函数
                tags = form.cleaned_data.pop('tags')
                content = form.cleaned_data.pop('content')
                content = XSSFilter().process(content)
                form.cleaned_data['blog_id'] = request.session['user_info']['blog__nid']
                obj = models.Article.objects.create(**form.cleaned_data)
                models.Article_Detail.objects.create(content=content, article=obj)
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(models.Article2Tag(article_id=obj.nid, tag_id=tag_id))
                models.Article2Tag.objects.bulk_create(tag_list)

            return redirect('/backend/article-0-0.html')
        else:
            return render(request, 'backend_add_article.html', {'form': form})
    else:
        return redirect('/')



















