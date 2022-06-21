"""
讲师:JasonJi    外号:鸡哥
邮箱:18817628568@163.com
微信:15618087189、18817628568(备注来源)
"""
from django import forms
from app01 import models


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=8, label='用户名',
                               error_messages={
                                   'min_length': '用户名最少三位',
                                   'max_length': '用户名最多八位',
                                   'required': '用户名不能为空'
                               },
                               widget=forms.widgets.TextInput(attrs={'class': 'form-control'})
                               )
    password = forms.CharField(min_length=3, max_length=8, label='密码',
                               error_messages={
                                   'min_length': '密码最少三位',
                                   'max_length': '密码最多八位',
                                   'required': '密码不能为空'
                               },
                               widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
                               )
    confirm_password = forms.CharField(min_length=3, max_length=8, label='确认密码',
                                       error_messages={
                                           'min_length': '确认密码最少三位',
                                           'max_length': '确认密码最多八位',
                                           'required': '确认密码不能为空'
                                       },
                                       widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
                                       )
    email = forms.EmailField(label='邮箱',
                             error_messages={
                                 'required': '邮箱不能为空',
                                 'invalid': '邮箱格式不正确'
                             },
                             widget=forms.widgets.EmailInput(attrs={'class': 'form-control'})
                             )
    '''针对用户头像字段 单独处理!!!'''
    # 局部钩子 校验用户名是否已存在
    def clean_username(self):
        username = self.cleaned_data.get('username')
        is_exist = models.UserInfo.objects.filter(username=username)
        if is_exist:
            self.add_error('username', '用户名已存在')
        return username

    # 全局钩子 校验两次密码是否一致
    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if not password == confirm_password:
            self.add_error('confirm_password', '两次密码不一致')
        return self.cleaned_data
