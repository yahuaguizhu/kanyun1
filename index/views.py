from django.shortcuts import render, HttpResponse
from django import views


class index(views.View):

    def get(self, request):

        request.session['Login'] = False
        return HttpResponse('hello su')


def square(request):
    return render(request, 'index/square.html')


def test(request):
    print(33333)
    return HttpResponse(444)

