# Generated by Django 2.2.3 on 2020-03-09 07:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='animal',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False, verbose_name='编号')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='昵称')),
                ('userid', models.CharField(max_length=20, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
            ],
            options={
                'verbose_name': '动物成员',
                'verbose_name_plural': '动物成员',
                'db_table': 'db_animal',
            },
        ),
        migrations.CreateModel(
            name='summary',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False, verbose_name='编号')),
                ('year', models.IntegerField(verbose_name='年份')),
                ('month', models.IntegerField(verbose_name='月份')),
                ('financeType', models.CharField(choices=[('income', '收入'), ('outcome', '支出')], max_length=20, verbose_name='收入/支出')),
                ('amount', models.FloatField(verbose_name='金额')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='finance.animal', to_field='name', verbose_name='成员')),
            ],
            options={
                'verbose_name': '财务小结',
                'verbose_name_plural': '财务小结',
                'db_table': 'db_summary',
            },
        ),
        migrations.CreateModel(
            name='detail',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False, verbose_name='编号')),
                ('time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='日期')),
                ('financeType', models.CharField(choices=[('income', '收入'), ('outcome', '支出')], max_length=20, verbose_name='收入/支出')),
                ('amount', models.FloatField(verbose_name='金额')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='finance.animal', to_field='name', verbose_name='成员')),
            ],
            options={
                'verbose_name': '财务记录',
                'verbose_name_plural': '财务记录',
                'db_table': 'db_logs',
            },
        ),
    ]
