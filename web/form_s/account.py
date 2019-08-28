from django.core.exceptions import ValidationError
from django import forms
from django.forms import fields

from .base import BaseForm

class LoginForm(BaseForm, forms.Form):
    username = fields.CharField(max_length=32, required=True)
    password = fields.CharField(max_length=32, min_length=8, required=True)
    rmb = fields.IntegerField(required=True)
    check_code = fields.CharField(
        error_messages={'required': '验证码不能为空'}
    )

    def clean_check_code(self):
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误', code='invalid')

class RegisterForm(BaseForm, forms.Form):
    username = fields.CharField(max_length=32, required=True)
    nickname = fields.CharField(max_length=32, required=True)
    email = fields.EmailField(max_length=32, required=True)
    password = fields.CharField(max_length=32, min_length=8, required=True)
    confirm_password = fields.CharField(max_length=32, min_length=8, required=True)
    check_code = fields.CharField(
        error_messages={'required': '验证码不能为空'}
    )

    def clean_check_code(self):
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误', code='invalid')

    def clean(self):
        v1 = self.cleaned_data['password']
        v2 = self.cleaned_data['confirm_password']
        if v1 == v2:
            return self.cleaned_data
        else:
            raise ValidationError('密码输入不一致')




























