# Generated by Django 2.1.7 on 2019-02-20 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='章节内容')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='书名')),
                ('introduction', models.CharField(max_length=300, verbose_name='简介')),
                ('general', models.TextField(default='暂无内容', verbose_name='概要')),
                ('mark', models.CharField(default='', max_length=40, verbose_name='文章标识')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('open', models.SmallIntegerField(default=1, verbose_name='书的可见性')),
                ('status', models.SmallIntegerField(default=0, verbose_name='发布状态')),
                ('price', models.FloatField(default=0, verbose_name='定价')),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='章节名称')),
                ('parent', models.IntegerField(verbose_name='父级章节')),
                ('status', models.SmallIntegerField(verbose_name='章节状态')),
            ],
        ),
        migrations.CreateModel(
            name='CommentFirst',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_time', models.DateTimeField(verbose_name='评论时间')),
                ('content', models.CharField(max_length=4000, verbose_name='评论内容')),
                ('status', models.SmallIntegerField(verbose_name='评论状态')),
            ],
        ),
        migrations.CreateModel(
            name='CommentSecond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_time', models.DateTimeField(verbose_name='评论时间')),
                ('content', models.CharField(max_length=4000, verbose_name='评论内容')),
                ('status', models.SmallIntegerField(verbose_name='评论状态')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='标签名称')),
            ],
        ),
    ]
