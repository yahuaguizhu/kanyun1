#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#

from django import forms
from .models import Book
from django.core.exceptions import ValidationError

class BookForm(forms.Form):
    name = forms.CharField(required=True, max_length=30, min_length=2, error_messages={
        'required': '名称为必填项',
        'max_length': '名称长度最大只能30个字符',
        'min_length': '名称长度最小要有2个字符'
    })

    # todo 文档标识一定要确保唯一
    mark = forms.RegexField(regex='^\w{10,40}$', required=True, error_messages={
        'invalid': '文档标识长度应在10-40个字符之间',
        'required': '文档标识为必填项',
    })

    def clean_mark(self):
        mark = self.cleaned_data.get('mark')
        if Book.objects.filter(mark=mark):
            raise ValidationError('文档标识已被使用')
        else:
            return mark

    introduction = forms.CharField(required=True, max_length=300, min_length=10, error_messages={
        'required': '简介为必填项',
        'max_length': '简介长度最大只能300个字符',
        'min_length': '简介长度最小要有10个字符'
    })

    open = forms.IntegerField(required=True, min_value=0, max_value=1, error_messages={
        'required': '文档可见性为必选项',
        'max_value': '文档可见性选择有误',
        'min_value': '文档可见性选择有误'
    })

















