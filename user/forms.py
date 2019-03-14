#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#

from django import forms
from django.core.exceptions import ValidationError
import re

# 编写自定义验证规则
def mobile_check(value):
    res = re.match('^1[356789]\d{9}$', value)
    if not res:
        # 自定义规则不抛异常表示通过
        raise ValidationError('手机号码格式错误')


def password_check(value, xxx):
    print(xxx)


class registerForm(forms.Form):
    mobile = forms.CharField(
        required=True,
        # 使用自定义验证规则
        validators=[mobile_check],
        error_messages={
            'required': '手机号为必填项',
        }
    )

    password = forms.CharField(
        required=True,
        max_length=12,
        min_length=6,
        error_messages={
            'required': '密码为必填项',
            'max_length': '密码长度最多不能超出12位',
            'min_length': '密码长度最小不能低于6位'
        },
        # widget=forms.TextInput(attrs={'class': 'xxxx', 'xxxx': 123})

    )

    password_confirm = forms.CharField(
        required=True,
        error_messages={
            'required': '重复密码为必填项',
        }
    )



    # 验证顺序是先验证某个字段设置的验证规则，紧接着执行该字段的局部钩子里面的验证代码，然后在执行其它字段的验证
    # def clean_mobile(self):
    #
    #     # if self.cleaned_data.get('mobile') == '13567890099':
    #     #     raise ValidationError('该手机号已经被注册')
    #     pass


    # clean 全局钩子 最后执行
    def clean(self):

        if self.cleaned_data.get('password') == self.cleaned_data.get('password_confirm'):
            pass
        else:
            raise ValidationError('两次密码输入不一致')






    # 首先定义验证form的规则
    # 执行验证
    # 如果验证成功，可以从验证结果中的cleaned_data中获取验证后的数据
    # 如果验证失败，可以从errors中获取错误信息







