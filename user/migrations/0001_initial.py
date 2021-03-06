# Generated by Django 2.1.7 on 2019-02-20 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buy_time', models.DateTimeField(verbose_name='购买时间')),
                ('cost', models.FloatField(verbose_name='费用')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='book.Book', verbose_name='书籍')),
            ],
        ),
        migrations.CreateModel(
            name='followRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follow_time', models.DateTimeField(verbose_name='关注时间')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Book', verbose_name='书籍')),
            ],
        ),
        migrations.CreateModel(
            name='Human',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=10, verbose_name='昵称')),
                ('account', models.CharField(max_length=20, verbose_name='用户名')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('mobile', models.CharField(max_length=11, verbose_name='手机号')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('register_time', models.DateTimeField(auto_now=True, verbose_name='注册时间')),
                ('status', models.SmallIntegerField(verbose_name='用户状态')),
            ],
        ),
        migrations.CreateModel(
            name='rewardRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buy_time', models.DateTimeField(verbose_name='打赏时间')),
                ('amount', models.FloatField(verbose_name='打赏数量')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='book.Book', verbose_name='书籍')),
                ('human', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.Human', verbose_name='打赏人')),
            ],
        ),
        migrations.AddField(
            model_name='followrecord',
            name='human',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Human', verbose_name='关注人'),
        ),
        migrations.AddField(
            model_name='buyrecord',
            name='human',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.Human', verbose_name='购买人'),
        ),
    ]
