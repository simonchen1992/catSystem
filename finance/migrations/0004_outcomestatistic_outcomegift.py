# Generated by Django 2.2.3 on 2021-09-06 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_outcomestatistic_outcomework'),
    ]

    operations = [
        migrations.AddField(
            model_name='outcomestatistic',
            name='outcomeGift',
            field=models.FloatField(default=0, verbose_name='礼物'),
        ),
    ]
