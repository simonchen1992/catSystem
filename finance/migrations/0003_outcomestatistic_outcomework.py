# Generated by Django 2.2.3 on 2021-09-03 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_auto_20200902_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='outcomestatistic',
            name='outcomeWork',
            field=models.FloatField(default=0, verbose_name='工作'),
        ),
    ]
