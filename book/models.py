from django.db import models
from user.models import Human



class Tag(models.Model):
    """电子书标签"""
    name = models.CharField(max_length=10, verbose_name='标签名称')

    def __str__(self):
        return self.name


# class Category(models.Model):
#     """电子书分类"""
#     name = models.CharField(max_length=10, verbose_name='图书分类')
#     parend = models.ForeignKey('self', verbose_name='父级分类', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name


class Book(models.Model):
    """电子书"""
    name = models.CharField(max_length=30, verbose_name='书名')
    introduction = models.CharField(max_length=300, verbose_name='简介')
    general = models.TextField(verbose_name='概要', default='暂无内容')
    mark = models.CharField(max_length=40, verbose_name='文章标识', default='')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now=True)
    open = models.SmallIntegerField(verbose_name='书的可见性', default=1)
    # 为0的时候表示未发布 1表示已发布 2表示被删除
    status = models.SmallIntegerField(verbose_name='发布状态', default=0)
    price = models.FloatField(verbose_name='定价', default=0)
    # 这里的作者，只是所有者
    owner = models.ForeignKey(Human, on_delete=models.CASCADE)
    # 书记和标签
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    # 图书的分类(分类下有图书的时候，不允许删除分类)
    # category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='图书分类')

    def __str__(self):
        return self.name


class Chapter(models.Model):
    """书籍的章节"""
    name = models.CharField(max_length=100, verbose_name='章节名称')
    parent = models.IntegerField(verbose_name='父级章节')
    # 书籍被删除，其对应的章节也一并删除
    # 章节可以有等级之分
    book = models.ForeignKey(Book, verbose_name='所属电子书', on_delete=models.CASCADE)
    # 一般0表示未显示到书中，1表示显示 2表示被删除
    status = models.SmallIntegerField(verbose_name='章节状态')

    # 为了不至于使当前表存储文件过大，这里将文章内容拆分成单独一张表
    # content = models.TextField(verbose_name='章节内容')

    def __str__(self):
        return self.name


class Article(models.Model):
    """书籍的各章节内容"""
    content = models.TextField(verbose_name='章节内容')
    chapter = models.OneToOneField(Chapter, verbose_name='所属章节', on_delete=models.CASCADE)


class CommentFirst(models.Model):
    """针对文章的一级评论"""
    comment_time = models.DateTimeField(verbose_name='评论时间')
    content = models.CharField(max_length=4000, verbose_name='评论内容')
    # 一般0表示正常，1表示被屏蔽 2表示被删除
    status = models.SmallIntegerField(verbose_name='评论状态')
    # 一般用户是不能被删除的，这里阻止用户被删除
    author = models.ForeignKey(Human, verbose_name='评论的作者', on_delete=models.PROTECT)
    # 章节的内容就是文章 评论是针对章节的
    # 主表被删的时候，可以一并删除也可以啥也不做，这里选择了啥也不做
    chapter = models.ForeignKey(Chapter, verbose_name='章节', on_delete=models.DO_NOTHING)


class CommentSecond(models.Model):
    """针对文章的一级评论进行评论的二级表"""
    comment_time = models.DateTimeField(verbose_name='评论时间')
    content = models.CharField(max_length=4000, verbose_name='评论内容')
    # 一般0表示正常，1表示被屏蔽 2表示被删除
    status = models.SmallIntegerField(verbose_name='评论状态')
    author = models.ForeignKey(Human, verbose_name='评论的作者', on_delete=models.PROTECT)
    # 支持针对一级评论的评论，也就是说，每个二级评论都必须针对一个一级评论
    # 一级评论被删除， 对应的二级评论也一并删除
    first = models.ForeignKey(CommentFirst, verbose_name='一级评论', on_delete=models.CASCADE)
    # 评论可以相互回复
    # 上级评论如果被删除，二级评论也一并删除
    reply = models.ForeignKey('self', verbose_name='回复的评论ID', on_delete=models.CASCADE)




