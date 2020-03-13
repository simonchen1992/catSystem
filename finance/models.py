from django.db import models
import django.utils.timezone as timezone



# Create your models here.

class User(models.Model):
	no = models.AutoField(primary_key=True, verbose_name='编号')
	userid = models.CharField(max_length=20,  verbose_name='用户名', unique=True)
	password = models.CharField(max_length=32, verbose_name='密码')
	def __str__(self):
		return self.userid
	class Meta:
		db_table = 'db_user'
		verbose_name = '管理员'
		verbose_name_plural = '管理员'


class Animal(models.Model):
	no = models.AutoField(primary_key=True, verbose_name='编号')
	name = models.CharField(max_length=20, verbose_name='昵称', unique=True)
	def __str__(self):
		return self.name
	class Meta:
		db_table = 'db_animal'
		verbose_name = '动物成员'
		verbose_name_plural = '动物成员'

class Summary(models.Model):
	no  = models.AutoField(primary_key=True, verbose_name='编号')
	year = models.IntegerField(verbose_name= '年份')
	month = models.IntegerField(verbose_name= '月份')
	updateTime = models.DateTimeField(auto_now= True, verbose_name='更改日期')
	catIncome = models.FloatField(verbose_name= '猫收入')
	catOutcome = models.FloatField(verbose_name='猫支出')
	mouseIncome = models.FloatField(verbose_name='鼠收入')
	mouseOutcome = models.FloatField(verbose_name='鼠支出')
	specialIncome = models.CharField(max_length=500, verbose_name='额外收入', default='')
	specialOutcome = models.CharField(max_length=500, verbose_name='额外支出', default='')
	remainFood = models.CharField(max_length=500, verbose_name='额外支出', default='')
	class Meta:
		db_table = 'db_summary'
		verbose_name = '财务小结'
		verbose_name_plural = '财务小结'
		constraints = [models.UniqueConstraint(fields=['year', 'month'], name='unique_period')]

class Detail(models.Model):
	no = models.AutoField(primary_key=True, verbose_name='编号')
	time = models.DateTimeField(default=timezone.now, verbose_name='日期')
	member = models.ForeignKey(Animal, on_delete=models.PROTECT, to_field='name', verbose_name='成员')
	financeType = models.CharField(max_length=20, choices=(('income', '收入'), ('outcome', '支出'),), verbose_name='收入/支出')
	amount = models.FloatField(verbose_name='金额')
	class Meta:
		db_table = 'db_logs'
		verbose_name = '财务记录'
		verbose_name_plural = '财务记录'