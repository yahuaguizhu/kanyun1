from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
import random, time, math, os, base64
from django import views
from .forms import registerForm
from .models import Human
from book.models import Book, Chapter, Article, Tag
# from django.core import serializers
from django.views.decorators.http import require_POST
# import _thread,time

class register(views.View):

    def post(self, request):

        # print(request.session['mobile_check_code'])
        # print(request.session['mobile_check_time'])
        #
        if request.POST['verify'] == request.session['mobile_check_code']:
            pass
        else:
            return JsonResponse({'code': 0, 'info': '验证码有误'})

        if time.time() >= request.session['mobile_check_time'] + 300:
            return JsonResponse({'code': 0, 'info': '验证码已过期'})
        else:
            pass

        # 使用我们定义好的验证form对传输过来的数据进行验证
        result = registerForm(request.POST)

        # 如果验证成功
        if result.is_valid():

            # 将验证后的数据插入到数据库中
            # todo 密码可以使用django自带的加密方式进行加密处理
            try:
                Human.objects.create(mobile=result.cleaned_data.get('mobile'),
                                     password=result.cleaned_data.get('password'), status=0)
            except Exception as e:
                return JsonResponse({'code': 0, 'info': '注册失败'})

            return JsonResponse({'code': 1, 'info': '成功'})

        else:
            # import json
            # return HttpResponse(json.dumps(result.errors))

            # return HttpResponse(result.errors.as_json())

            return JsonResponse({'code': 2, 'info': result.errors})

            # return render(request, 'user/register.html', {'xxx': result})

        # print(result.errors)
        #
        # print(result.cleaned_data)

    def get(self, request):

        obj = registerForm()
        return render(request, 'user/register.html', {'obj': obj})

def send_sms(request):
    """用户注册的时候发送验证码"""
    appid = 1400170241  # SDK AppID是1400开头
    # 短信应用SDK AppKey
    appkey = "9ecace73ca78cfbcf1178e135c368a55"
    # 需要发送短信的手机号码

    phone_numbers = request.POST['mobile']
    # todo 对手机号的合法型进行验证
    # todo 短信发送数量的限制

    # 在腾讯云那里申请到的短信模板的ID
    template_id = 245450

    # 签名，我们在腾讯云哪里申请获得批准后的一个签名
    sms_sign = "书生主页"

    # 短信类型 {0: 普通短信, 1: 营销短信}，可以在腾讯云 短信正文 - 类型 那里看到
    # sms_type = 0

    # 指定模板id进行单条短信发送
    from qcloudsms_py import SmsSingleSender
    from qcloudsms_py.httpclient import HTTPError

    ssender = SmsSingleSender(appid, appkey)
    # 参数，就是我们在申请短信模板的时候，预留的可以替换成参数的位置
    code = str(random.randint(1000, 9999))
    params = [code, 5]
    try:
        # 参数1 国家码，86表示中国
        # 参数2 接收短信的手机号
        # 参数3 要发送的短信模板id
        # 参数4 短信模板的中参数（这里相当于传了实参）
        # 参数5 短信签名（关键字参数)
        result = ssender.send_with_param(86, phone_numbers, template_id, params, sign=sms_sign, extend="", ext="")
    except HTTPError as e:
        return JsonResponse({'code': 0, 'info': '发送失败'})
    except Exception as e:
        return JsonResponse({'code': 0, 'info': '发送失败'})

    request.session['mobile_check_code'] = code
    request.session['mobile_check_time'] = time.time()
    return JsonResponse({'code': 1, 'info': '短信发送成功'})



class login(views.View):
    def get(self, request):

        return render(request, 'user/login.html')

    def post(self, request):
        # todo 数据验证
        h = Human.objects.filter(mobile=request.POST['mobile']).values()[0]
        h['register_time'] = h['register_time'].strftime('%Y-%m-%d %H:%M:%S')

        if h['password'] == request.POST['password']:

            request.session['Login'] = h
            return redirect(reverse('index:square'))
        else:
            return HttpResponse('用户名或者密码错误')


def logout(request):
    request.session['Login'] = False
    return redirect(reverse('index:square'))

def doc_list(request, page=1):
    num = 10

    # 总共多少页
    total = math.ceil(Book.objects.count() // num)

    # 当前页展示的数据

    # limit偏移量计算
    x = (page - 1) * num

    # print(Book.objects.all()[1:3])
    # book_lists = Book.objects.filter(owner=request.session['Login']['id'])

    book_lists = Book.objects.raw('select * from book_book where owner_id=%s order by id DESC limit %s, %s' % (request.session['Login']['id'], x , num))

    # page_string = ''
    # if total <= 9:
    #     for i in range(1, total+1):
    #         if page == i:
    #             page_string = page_string + '<div class="active item">' + str(i) + '</div>'
    #         else:
    #             page_string = page_string + '<a class="item" href="%s">%s</a>' % (reverse("user:user_doc_lists", args=(i,)), i)
    #
    # elif total > 9:
    #     if page > 5 and page < (total-4):
    #
    #         for i in range(page-4, page):
    #             page_string = page_string + '<a class="item" href="%s">%s</a>' % (
    #                 reverse("user:user_doc_lists", args=(i,)), i)
    #         page_string = page_string + '<div class="active item">' + str(page) + '</div>'
    #         for i in range(page+1, page + 5):
    #             page_string = page_string + '<a class="item" href="%s">%s</a>' % (
    #                 reverse("user:user_doc_lists", args=(i,)), i)
    #     elif page > 5 and page > (total-5):
    #         # 当前页在最后9页的中间页以后的时候
    #         for i in range(total-9, total + 1):
    #             if page == i:
    #                 page_string = page_string + '<div class="active item">' + str(i) + '</div>'
    #             else:
    #                 page_string = page_string + '<a class="item" href="%s">%s</a>' % (
    #                 reverse("user:user_doc_lists", args=(i,)), i)
    #     else:
    #         for i in range(1, 10):
    #             if page == i:
    #                 page_string = page_string + '<div class="active item">' + str(i) + '</div>'
    #             else:
    #                 page_string = page_string + '<a class="item" href="%s">%s</a>' % (
    #                 reverse("user:user_doc_lists", args=(i,)), i)
    #


    # ps = '<a class="item" href="%s">首页</a>' % (reverse("user:user_doc_lists", args=(1,)))
    #
    # if page >= 5 and page < (total - 4):
    #     for i in range(page - 4, page):
    #         ps = ps + '<a class="item" href="%s">%s</a>' % (reverse("user:user_doc_lists", args=(i,)), i)
    #     ps = ps + '<div class="active item">' + str(page) + '</div>'
    #     for i in range(page + 1, page + 5):
    #         ps = ps + '<a class="item" href="%s">%s</a>' % (reverse("user:user_doc_lists", args=(i,)), i)
    # else:
    #     if page >= total - 4:
    #         if total > 9:
    #             start = total-8
    #         else:
    #             start = 1
    #         for i in range(start, total+1):
    #             if page == i:
    #                 ps = ps + '<div class="active item">' + str(i) + '</div>'
    #             else:
    #                 ps = ps + '<a class="item" href="%s">%s</a>' % (reverse("user:user_doc_lists", args=(i,)), i)
    #     else:
    #         if total >= 9:
    #             end = 9 + 1
    #         else:
    #             end = total + 1
    #         for i in range(1, end):
    #             if page == i:
    #                 ps = ps + '<div class="active item">' + str(i) + '</div>'
    #             else:
    #                 ps = ps + '<a class="item" href="%s">%s</a>' % (reverse("user:user_doc_lists", args=(i,)), i)
    #
    #
    #
    #
    # ps = ps + '<a class="item" href="%s">尾页</a>' % ( reverse("user:user_doc_lists", args=(total,)))

    from xx_fun import pages



    # return render(request, 'user/doc_list.html', {'lists': book_lists, 'page_raw': page_string})
    # return render(request, 'user/doc_list.html', {'lists': book_lists, 'page_raw': ps})
    return render(request, 'user/doc_list.html', {'lists': book_lists, 'page_raw': pages(total, page, "user:user_doc_lists")})


class create_content(views.View):

    def get(self, request, id, cid=0):

        """
        :param request:
        :param id: 图书的id
        :param cid: 章节的id
        :return:
        """

        # 如果用户试图编辑一个不存在的文档
        try:
            b = Book.objects.get(id=id)
        except Exception as e:
            return redirect(reverse('user:user_doc_lists'))

        # 如果用户试图操作一个不属于自己的文档
        if b.owner_id != request.session['Login']['id']:
            # 如果要创作的书不属于当前登录用户
            return redirect(reverse('user:user_doc_lists'))

        # 获取本书的所有章节
        lists = Chapter.objects.filter(book_id=id).values()
        res = format_tree(lists)

        if not cid:
            b = Book.objects.get(id=id)
            content = b.general

        else:
            # 尝试获取当前章节的内容
            try:
                a = Article.objects.get(chapter_id=cid)
                content = a.content
            except Exception as e:
                content = ''

        return render(request, 'user/editor.html', {'id': id, 'lists': res, 'cid': cid, 'content': content})


@require_POST
def create_chapter(request):
    # 书的id
    id = request.POST['id']
    #要创建的章节的名称
    name = request.POST['name']

    try:
        parent = request.POST['parent']
    except Exception as e:
        parent = 0
    # todo 数据格式验证
    try:
        c = Chapter.objects.create(name=name, parent=parent, status=0, book_id=id)
    except Exception as e:
        return JsonResponse({'code': 0, 'info': '创建失败，请重试！'})
    # return JsonResponse({'id': c.id, 'code': 1, 'info': '创建成功'})
    return JsonResponse({'url': reverse('user:create_content', args=(id, c.id)), 'code': 1, 'info': '创建成功'})


def create_chapter_form(request, id, cid):
    """
    接收的参数代表的意义
    id ： 书的id
    cid ： 书的章节id
    """

    if cid == 0:
        return render(request, 'user/create_chapter_form.html', {'id': id})

    # 如果用户试图编辑一个不存在的文档
    try:
        b = Book.objects.get(id=id)
    except Exception as e:
        return redirect(reverse('user:user_doc_lists'))

    # 如果用户试图操作一个不属于自己的文档
    if b.owner_id != request.session['Login']['id']:
        return redirect(reverse('user:user_doc_lists'))

    # 获取章节的id
    try:
        ch = Chapter.objects.get(id=cid)
    except Exception as e:
        # 如果章节不存在，则直接跳到创建图书简介
        return redirect(reverse('user:create_content', args=(id, 0)))

    if ch.book_id != id:
        # 如果当前的章节不属于当前传来的书，说明是非法操作，直接跳到个人的文档列表
        return redirect(reverse('user:create_content', args=(id, 0)))
    return render(request, 'user/create_chapter_form.html', {'id': id, 'ch': ch})


def format_tree(data, parent=0):
    newData = []
    for v in data:
        # 父级章节在所有的章节中 一个一个的看是不是自己的子级
        if v['parent'] == parent:
            # 在你回到父亲臂膀下之前把你的儿子找回来
            v['nodes'] = format_tree(data, v['id'])
            newData.append(v)
    return newData



@require_POST
def add_content(request):
    content = request.POST['content']
    cid = request.POST['cid']
    if cid == '0':
        # 添加概要
        try:
            book_id = request.POST['book']
            Book.objects.filter(id=book_id).update(general=content)
            return JsonResponse({'code': 1})
        except Exception as e:
            return JsonResponse({'code': e})
    else:
        # 添加章节的内容
        try:
            Article.objects.update_or_create(chapter_id=cid, defaults={'content': content})
        except Exception as e:
            return JsonResponse({'code': 0})
        try:
            status = request.POST['status']
            if status:
                Chapter.objects.filter(id=cid).update(status=1)
        except Exception as e:
            pass

        return JsonResponse({'code': 1})



class book_set(views.View):

    def get(self, request, id):

        try:
            book = Book.objects.get(id=id)
        except Exception as e:
            return render(request, 'user/error.html', {'error_info': '非法操作'})
        # 如果用户试图操作一个不属于自己的文档
        if book.owner_id != request.session['Login']['id']:
            return render(request, 'user/error.html', {'error_info': '您没有权限进行本操作！'})


        # 读出该文档的标签
        tags = book.tags.all().order_by('-id')
        return render(request, 'user/book_set.html', {'book': book, 'tags': tags})

    def post(self, request, id):
        name = request.POST['title']
        introduction = request.POST['description']
        id = request.POST['id']

        # todo 数据验证

        try:
            Book.objects.filter(id=id).update(name=name, introduction=introduction)
        except Exception as e:
            return render(request, 'user/error.html', {'error_info': '操作失败！'})

        # return redirect(reverse('user:book_set', args=(id,)))

        return render(request, 'common/jump.html', {'info': '操作成功', 'url': reverse('user:book_set', args=(id,))})

@require_POST
def add_book_tag(request):

    keyword = request.POST['keyword']

    if len(keyword) > 6:
        return JsonResponse({"code": 0, 'info': '标签最大只能有6个字符'})

    book_id = request.POST['book_id']
    # todo  数据验证

    tag = Tag.objects.get_or_create(name=keyword)

    try:
        book = Book.objects.get(id=book_id)
    except Exception as e:
        return JsonResponse({"code": 0, 'info': '非法操作'})
    num1 = book.tags.count()
    if num1 <= 10:
        try:
            book.tags.add(tag[0])
        except Exception as e:
            return JsonResponse({"code": 0, 'info': '添加失败'})
        num2 = book.tags.count()

        if num1 == num2:
            return JsonResponse({"code": 0, 'info': '该标签已存在'})
        else:
            return JsonResponse({"code": 1, 'info': '添加成功'})
    else:
        return JsonResponse({"code": 0, 'info': '每本书最多只能有10个标签'})

@require_POST
def delete_book_tag(request):
    book_id = request.POST['book']
    tag = request.POST['tag']
    # todo 数据的验证
    try:
        book = Book.objects.get(id=book_id)
    except Exception as e:
        return JsonResponse({'code': 0, 'info': '非法操作'})
    # 如果用户试图操作一个不属于自己的文档
    if book.owner_id != request.session['Login']['id']:
        return JsonResponse({'code': 0, 'info': '您没有权限进行本操作'})

    num1 = book.tags.count()
    book.tags.remove(Tag.objects.get(id=tag))
    num2 = book.tags.count()

    if num1 > num2:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0, 'info': '删除失败'})

class modify(views.View):
    def get(self, request):
        uid = request.session['Login']['id']
        human = Human.objects.get(id=uid)
        return render(request,'user/modify.html',{'human':human, 'menu_style':'modify'})

    def post(self, request):
        return redirect(reverse('user:modify'))
def upload_avatar(request):
    if request.method == "GET":
        return render(request, 'user/upload_avatar.html')

    if request.method == "POST":
        uid = request.session['Login']['id']
        #获取img base64码
        strs = request.POST['img']
        #获取img name名称
        name = request.POST['name']
        #todo 数据验证

        #获取文件的原来后缀名 分割
        ext = name.split('.')[-1:][0]
        #拼接路径  获取时间
        min_dir = 'user/' + time.strftime("%Y-%m-%d", time.localtime())
        dir = 'static/' + min_dir

        #判断目录是否存在
        if not os.path.exists(dir):
            os.mkdir(dir)
        file_name = str(time.time()) + str(uid) + '.' + ext
        imgdata = base64.b64decode(strs.split('base64,')[1])
        file = open(os.path.join(dir, file_name), 'wb')
        try:
            file.write(imgdata)
            Human.objects.filter(id=uid).update(avatar=os.path.join(min_dir, file_name))
            return JsonResponse({'code':1})
        except Exception as e:
            return JsonResponse({'code':0})



