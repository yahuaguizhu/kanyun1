from django.shortcuts import render, HttpResponse, redirect, reverse
from django.http.response import HttpResponseNotFound
from django import views
from .forms import BookForm
from .models import Book
from user.models import Human


class create(views.View):

    def get(self, request):
        return render(request, 'book/create.html')


    def post(self, request):
        return HttpResponse(1)


def create(request):
    if request.method == "POST":
        # print(request.POST)

        # 使用我们定义的From类进行验证数据
        result = BookForm(request.POST)
        # 如果验证通过
        if result.is_valid():
            # 读取验证后的数据
            data = result.cleaned_data
        else:
            # 如果验证失败，响应对应页面和错误信息
            return render(request, 'book/create.html', {'error': result.errors})

        # 添加一些需要自己处理的一些数据
        data['owner'] = Human.objects.get(id=request.session['Login']['id'])

        if Book.objects.create(**data):
            return redirect(reverse('user:user_doc_lists'))
        else:
            return render(request, 'book/create.html', {'createError': '文档创建失败'})
    elif request.method == 'GET':
        return render(request, 'book/create.html')
    else:
        return HttpResponseNotFound()
