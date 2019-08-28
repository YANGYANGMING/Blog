import json
from repository import models
from io import BytesIO
from utils.check_code import create_validate_code  #生成验证码
from django.shortcuts import render, redirect, HttpResponse
from ..form_s.account import LoginForm, RegisterForm


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        print(form)
        result = {'status': False, 'message': None, 'data': None}
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_info = models.UserInfo.objects.\
                filter(username=username, password=password).\
                values('nid', 'nickname',
                       'username', 'email',
                       'blog__nid',
                       'blog__site'
                       ).first()
            if not user_info:
                result['message'] = '用户名或密码错误'
            else:
                result['status'] = True
                request.session['user_info'] = user_info
                if form.cleaned_data['rmb']:
                    print(form.cleaned_data['rmb'])
                    request.session.set_expiry(60 * 60 * 24 * 30)
        else:
            print(form.errors)
            if 'check_code' in form.errors:
                result['message'] = '验证码错误或者过期'
            else:
                result['message'] = '用户名或密码错误'
        return HttpResponse(json.dumps(result))

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        form = RegisterForm(request=request, data=request.POST)
        result = {'status': False, 'message': None, 'data': None}
        if form.is_valid():
            result['status'] = True
            username = form.cleaned_data['username']
            nickname = form.cleaned_data['nickname']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            models.UserInfo.objects.create(
                username=username,
                nickname=nickname,
                password=password,
                email=email,
            )
        else:
            return render(request, 'login.html')

        return render(request, 'home.html')

def logout(request):

    request.session.clear()
    return redirect('/index.html/')

def check_code(request):
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')  #把img图片对象写到stream内存里
    request.session['CheckCode'] = code
    print(code)
    return HttpResponse(stream.getvalue())









