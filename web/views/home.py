from django.shortcuts import render, redirect
from utils.pagination import Pagination
from utils.pagination1 import Pagination1
from repository import models
from django.urls import reverse


def index(request, *args, **kwargs):
    """
    博客首页，展示全部博文
    :param request:
    :return:
    """
    article_type_list = models.Article.type_choices
    if kwargs:
        article_type_id = int(kwargs['article_type_id'])
        base_url = reverse('index', kwargs=kwargs)    #all/1.html
    else:
        article_type_id = None
        base_url = '/'

    data_count = models.Article.objects.filter(**kwargs).count()

    page_obj = Pagination(request.GET.get('p'), data_count)
    article_list = models.Article.objects.filter(**kwargs).order_by('-nid')[page_obj.start:page_obj.end]
    page_str = page_obj.page_str(base_url)

    return render(request, 'index.html', locals())

def home(request, site):
    """
    博主个人首页
    :param request:
    :param site: 博主的网站后缀如：http://xxx.com/wupeiqi.html
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        return redirect('/')
    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)

    date_list = models.Article.objects.raw(
        "select nid, count(nid) as num,date_format(create_time,'%%Y-%%m') as ctime from repository_article group by date_format(create_time,'%%Y-%%m')"
    )

    article_list = models.Article.objects.filter(blog=blog).order_by('-nid').all()

    return render(request, 'home.html', locals())


def filter(request, site, condition, val):
    """
    分类显示
    :param request:
    :param site:
    :param condition:
    :param val:
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        print(blog)
        return redirect('/')
    # tag_list = models.Tag.objects.filter(blog=blog)
    # category_list = models.Category.objects.filter(blog=blog)
    # date_list = models.Article.objects.raw(
    #     'select nid, count(nid) as num,DATE_FORMAT(create_time, "%%Y-%%m") as ctime from repository_article group by DATE_FORMAT(create_time, "%%Y-%%m")')

    template_name = "home_summary_list.html"
    if condition == 'tag':
        template_name = "home_title_list.html"
        article_list = models.Article.objects.filter(tags=val, blog=blog).all()

    elif condition == 'category':
        template_name = "home_summary_list.html"
        article_list = models.Article.objects.filter(category_id=val, blog=blog)

    elif condition == 'date':
        template_name = "home_summary_list.html"
        article_list = models.Article.objects.filter(blog=blog).extra(
            where=["date_format(create_time,'%%Y-%%m')=%s"], params=[val, ]).all()

    else:
        template_name = []

    return render(request, template_name, locals())




def detail(request, site, nid, *args, **kwargs):
    blog = models.Blog.objects.filter(site=site).select_related('user').first()

    article = models.Article.objects.filter(blog=blog, nid=nid).select_related('category', 'article_detail').first()
    comment_list = models.Comment.objects.filter(article=article).select_related('reply')

    data_count = models.Comment.objects.filter(**kwargs).count()

    page_obj = Pagination1(request.GET.get('comment_p'), data_count)
    comment_list1 = models.Comment.objects.filter(**kwargs).order_by('-nid')[page_obj.start:page_obj.end]
    page_str = page_obj.page_str()

    return render(request, 'home_detail.html', locals())





