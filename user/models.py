from django.db import models
# from book.models import Book


class Human(models.Model):
    """网站的用户"""
    nickname = models.CharField(max_length=10, verbose_name='昵称')
    account = models.CharField(max_length=20, verbose_name='用户名')
    email = models.EmailField(verbose_name='邮箱')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    password = models.CharField(max_length=32, verbose_name='密码')
    register_time = models.DateTimeField(verbose_name='注册时间', auto_now=True)
    # 用户状态， 0表示正常 1表示封号 等等
    status = models.SmallIntegerField(verbose_name='用户状态')
    avatar = models.CharField(max_length=100, verbose_name='用户头像' , default='')
    # 其它字段可以自行设置

    def __str__(self):
        return self.nickname


class BuyRecord(models.Model):
    """用户购买图书的记录"""
    buy_time = models.DateTimeField(verbose_name='购买时间')
    cost = models.FloatField(verbose_name='费用')
    # 购买的图书 （图书一旦被人购买过，就不能被删除，只能下架）
    book = models.ForeignKey('book.Book', on_delete=models.PROTECT, verbose_name='书籍')
    # 用户只要购买过书籍就只能封号，不能被删除
    human = models.ForeignKey(Human, on_delete=models.PROTECT, verbose_name='购买人')


class followRecord(models.Model):
    """关注记录"""
    follow_time = models.DateTimeField(verbose_name='关注时间')
    # 关注的图书一旦被删除，对应的关注记录也会被删除
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE, verbose_name='书籍')
    # 购买人
    human = models.ForeignKey(Human, on_delete=models.CASCADE, verbose_name='关注人')


class rewardRecord(models.Model):
    """打赏记录"""
    buy_time = models.DateTimeField(verbose_name='打赏时间')
    amount = models.FloatField(verbose_name='打赏数量')
    # 购买的图书 （图书一旦被人打赏过，就不能被删除，只能下架）
    book = models.ForeignKey('book.Book', on_delete=models.PROTECT, verbose_name='书籍')
    # 用户只要打赏过书籍就只能封号，不能被删除
    human = models.ForeignKey(Human, on_delete=models.PROTECT, verbose_name='打赏人')



