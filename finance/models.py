from django.db import models
import django.utils.timezone as timezone

# Create your models here.


class animal(models.Model):
	no = models.AutoField(primary_key=True, verbose_name='编号')
	name = models.CharField(max_length=20, verbose_name='昵称', unique=True)
	def __str__(self):
		return self.name
	
	class Meta:
		db_table = 'db_animal'
		verbose_name = '动物成员'
		verbose_name_plural = '动物成员'

class summary(models.Model):
	no  = models.AutoField(primary_key=True, verbose_name='编号')
	year = models.IntegerField(verbose_name= '年份')
	month = models.IntegerField(verbose_name= '月份')
	member = models.ForeignKey(animal, on_delete=models.PROTECT, to_field='name', verbose_name= '成员')
	financeType = models.CharField(max_length=20, choices=(('income', '收入'), ('outcome', '支出'),), verbose_name= '收入/支出')
	amount = models.FloatField(verbose_name= '金额')
	
	
	class Meta:
		db_table = 'db_summary'
		verbose_name = '财务小结'
		verbose_name_plural = '财务小结'

class detail(models.Model):
	no = models.AutoField(primary_key=True, verbose_name='编号')
	time = models.DateTimeField(default=timezone.now, verbose_name='日期')
	member = models.ForeignKey(animal, on_delete=models.PROTECT, to_field='name', verbose_name='成员')
	financeType = models.CharField(max_length=20, choices=(('income', '收入'), ('outcome', '支出'),), verbose_name='收入/支出')
	amount = models.FloatField(verbose_name='金额')
	class Meta:
		db_table = 'db_logs'
		verbose_name = '财务记录'
		verbose_name_plural = '财务记录'