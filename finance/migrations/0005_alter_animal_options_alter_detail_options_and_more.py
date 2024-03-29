# Generated by Django 4.2.10 on 2024-03-08 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_outcomestatistic_outcomegift'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='animal',
            options={'verbose_name': '动物成员'},
        ),
        migrations.AlterModelOptions(
            name='detail',
            options={'verbose_name': '财务记录'},
        ),
        migrations.AlterModelOptions(
            name='incomestatistic',
            options={'verbose_name': '财务统计(收入)'},
        ),
        migrations.AlterModelOptions(
            name='outcomestatistic',
            options={'verbose_name': '财务统计(支出)'},
        ),
        migrations.AlterModelOptions(
            name='summary',
            options={'verbose_name': '财务小结'},
        ),
        migrations.AlterModelOptions(
            name='type',
            options={'verbose_name': '食物种类'},
        ),
        migrations.AddField(
            model_name='incomestatistic',
            name='incomeBaby',
            field=models.FloatField(default=0, verbose_name='派派红包'),
        ),
        migrations.AddField(
            model_name='outcomestatistic',
            name='outcomeFamBaby',
            field=models.FloatField(default=0, verbose_name='派派'),
        ),
        migrations.AddField(
            model_name='outcomestatistic',
            name='outcomeMedical',
            field=models.FloatField(default=0, verbose_name='医疗'),
        ),
        migrations.AlterField(
            model_name='detail',
            name='foodType',
            field=models.ForeignKey(db_column='foodType', on_delete=django.db.models.deletion.PROTECT, to='finance.type', to_field='foodType', verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='detail',
            name='member',
            field=models.ForeignKey(db_column='member', on_delete=django.db.models.deletion.PROTECT, related_name='details', to='finance.animal', to_field='name', verbose_name='成员'),
        ),
        migrations.AlterField(
            model_name='incomestatistic',
            name='member',
            field=models.ForeignKey(db_column='member', on_delete=django.db.models.deletion.PROTECT, to='finance.animal', to_field='name'),
        ),
        migrations.AlterField(
            model_name='outcomestatistic',
            name='member',
            field=models.ForeignKey(db_column='member', on_delete=django.db.models.deletion.PROTECT, to='finance.animal', to_field='name'),
        ),
    ]
