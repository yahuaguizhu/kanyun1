#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#


from django.utils.deprecation import MiddlewareMixin

class LoginMiddle(MiddlewareMixin):

    def process_request(self, request):
        # print(1)
        pass


class XXX(MiddlewareMixin):
    def process_request(self, request):
        # print(2)
        pass


















