#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
from django.urls import reverse



def pages(total, page, route):

    ps = '<a class="item" href="%s">首页</a>' % (reverse(route, args=(1,)))
    if page >= 5 and page < (total - 4):
        for i in range(page - 4, page):
            ps = ps + '<a class="item" href="%s">%s</a>' % (reverse(route, args=(i,)), i)
        ps = ps + '<div class="active item">' + str(page) + '</div>'
        for i in range(page + 1, page + 5):
            ps = ps + '<a class="item" href="%s">%s</a>' % (reverse(route, args=(i,)), i)
    else:
        if page >= total - 4:
            if total > 9:
                start = total - 8
            else:
                start = 1
            for i in range(start, total + 1):
                if page == i:
                    ps = ps + '<div class="active item">' + str(i) + '</div>'
                else:
                    ps = ps + '<a class="item" href="%s">%s</a>' % (reverse(route, args=(i,)), i)
        else:
            if total >= 9:
                end = 9 + 1
            else:
                end = total + 1
            for i in range(1, end):
                if page == i:
                    ps = ps + '<div class="active item">' + str(i) + '</div>'
                else:
                    ps = ps + '<a class="item" href="%s">%s</a>' % (reverse(route, args=(i,)), i)

    ps = ps + '<a class="item" href="%s">尾页</a>' % (reverse(route, args=(total,)))
    return ps
















