from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from django.db import connection
from repository import models

from django.forms import Form
from django.forms import fields
from django.forms import widgets
from datetime import datetime

import datetime
import json

def trouble_list(request):
    # user_info = request.session.get['user_info']
    current_user_id = request.session.get('user_info')['nid']
    result = models.Trouble.objects.filter(user_id=current_user_id).order_by('status').\
        only('title', 'status', 'processor', 'create_time', 'evaluate')

    return render(request, 'backend_trouble_list.html', locals())


class TroubleMaker(Form):
    title = fields.CharField(
        max_length=32,
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    detail = fields.CharField(
        widget=widgets.Textarea(attrs={'id': 'detail', 'class': 'kind-content'})
    )


def trouble_create(request):
    if request.method == "GET":
        form = TroubleMaker()
    elif request.method == "POST":
        form = TroubleMaker(data=request.POST)
        if form.is_valid():
            # form.cleaned_data

            dic = {}
            dic['user_id'] = request.session.get('user_info')['nid']
            dic['create_time'] = datetime.datetime.now()
            dic['status'] = 1
            dic.update(form.cleaned_data)
            models.Trouble.objects.create(**dic)
            return redirect('/backend/trouble-list.html')

    return render(request, 'backend_trouble_create.html', locals())


def trouble_edit(request, nid):
    if request.method == "GET":
        obj = models.Trouble.objects.filter(nid=nid, status=1).only('nid', 'title', 'detail').first()
        if not obj:
            return HttpResponse('已处理中的报障单无法修改！')
        #initial只做初始化，不做错误信息展示
        form = TroubleMaker(initial={'title': obj.title, 'detail': obj.detail})
        #加上initial表示后面不会因为errors而进行form验证，则在title数据为空时不会报错，使用data会显示报错
        return render(request, 'backend_trouble_edit.html', {'form': form, 'nid': nid})
    elif request.method == "POST":
        form = TroubleMaker(request.POST)  #data=request.POST, files=request.FILES
        if form.is_valid():
            v = models.Trouble.objects.filter(nid=nid, status=1).update(**form.cleaned_data)
            #v表示已修改的条数
            if not v:
                return HttpResponse('已经被处理')
            else:
                return redirect('/backend/trouble-list.html')
        else:
            return render(request, 'backend_trouble_edit.html', {'form': form, 'nid': nid})

def trouble_kill_list(request):
    current_user_id = request.session.get('user_info')['nid']
    result = models.Trouble.objects.filter(Q(processor_id=current_user_id)|Q(status=1)).order_by('status')
    return render(request, 'backend_trouble_kill_list.html', locals())


class TroubleKill(Form):
    solution = fields.CharField(
        widget=widgets.Textarea(attrs={'id': 'solution', 'class': 'kind-content'})
    )


def trouble_kill(request, nid):
    current_user_id = request.session.get('user_info')['nid']
    question_obj = models.Tpl.objects.all()
    if request.method == "GET":
        ret = models.Trouble.objects.filter(nid=nid, processor_id=current_user_id).count()
        #以前没抢到
        if not ret:
            v = models.Trouble.objects.filter(nid=nid, status=1).update(processor_id=current_user_id, status=2)
            if not v:
                return HttpResponse('手速太慢了...')

        obj = models.Trouble.objects.filter(nid=nid).first()
        form = TroubleKill(initial={'title': obj.title, 'solution': obj.solution})
        return render(request, 'backend_trouble_kill.html', locals())
    elif request.method == "POST":
        #防止他人处理自己已经抢到的单子，或者防止自己重新修改已提交的单子
        ret = models.Trouble.objects.filter(nid=nid, processor_id=current_user_id, status=2).count()
        if not ret:
            return HttpResponse('问题已解决')

        form = TroubleKill(request.POST)
        if form.is_valid():
            dic = {}
            dic['status'] = 3
            dic['solution'] = form.cleaned_data['solution']
            dic['process_time'] = datetime.datetime.now()
            v = models.Trouble.objects.filter(nid=nid, processor_id=current_user_id, status=2).update(**dic)
            return redirect('/backend/trouble-kill-list.html')
        else:
            obj = models.Trouble.objects.filter(nid=nid).first()
            return render(request, 'backend_trouble_kill.html', locals())

def trouble_ajax(request):
    nid = request.GET.get('v')
    ret = {'status': True, 'data': None, 'message': None}
    ret['data'] = models.Tpl.objects.filter(id=nid).values('content').first()
    return HttpResponse(json.dumps(ret))


def trouble_evaluate(request, nid):
    current_user_id = request.session.get('user_info')['nid']
    evaluate_list = models.Trouble.evaluate_choices
    if request.method == "GET":
        obj = models.Trouble.objects.filter(nid=nid, user=current_user_id).only('nid', 'title', 'solution').first()
        return render(request, 'backend_trouble_evaluate.html', locals())
    else:
        ret = request.POST.get('evaluate')
        v = models.Trouble.objects.filter(nid=nid, user_id=current_user_id).update(evaluate=ret)
        if not v:
            return render(request, 'backend_trouble_evaluate.html', locals())
        else:
            return redirect('/backend/trouble-list.html')


def trouble_report(request):
    return render(request, 'backend_trouble_report.html')


def trouble_json_report(request):
    #从数据库中获取数据
    user_list = models.UserInfo.objects.filter()
    response = []
    for user in user_list:
        cursor = connection.cursor()
        cursor.execute("""select date_format(date_format(create_time,'%%Y-%%m-01'),'%%s')*1000,count(nid) from repository_trouble where processor_id = %s group by date_format(create_time,'%%Y-%%m')""",[user.nid])
        result = cursor.fetchall()
        temp = {
            'name': user.username,
            'data': result
        }
        response.append(temp)

    return HttpResponse(json.dumps(response))















