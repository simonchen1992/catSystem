# Generated by Django 2.2.3 on 2020-03-11 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_auto_20200311_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='catIncome',
            field=models.FloatField(verbose_name='猫收入'),
        ),
        migrations.AlterField(
            model_name='summary',
            name='catOutcome',
            field=models.FloatField(verbose_name='猫支出'),
        ),
        migrations.AlterField(
            model_name='summary',
            name='mouseIncome',
            field=models.FloatField(verbose_name='鼠收入'),
        ),
        migrations.AlterField(
            model_name='summary',
            name='mouseOutcome',
            field=models.FloatField(verbose_name='鼠支出'),
        ),
        migrations.AlterField(
            model_name='summary',
            name='remainFood',
            field=models.CharField(max_length=500, verbose_name='额外支出'),
        ),
        migrations.AlterField(
            model_name='summary',
            name='specialIncome',
            field=models.CharField(max_length=500, verbose_name='额外收入'),
        ),
        migrations.AlterField(
            model_name='summary',
            name='specialOutcome',
            field=models.CharField(max_length=500, verbose_name='额外支出'),
        ),
    ]
