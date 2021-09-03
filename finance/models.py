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
		
		
class Type(models.Model):
	no = models.AutoField(primary_key=True, verbose_name='编号')
	financeType = models.CharField(max_length=20, choices=(('income', '收入'), ('outcome', '支出'),), verbose_name='收入/支出')
	foodType = models.CharField(max_length=500, verbose_name='类型', unique=True, default='')
	class Meta:
		db_table = 'db_type'
		verbose_name = '食物种类'
		verbose_name_plural = '食物种类'

class Summary(models.Model):
	no  = models.AutoField(primary_key=True, verbose_name='编号')
	year = models.IntegerField(verbose_name= '年份')
	month = models.IntegerField(verbose_name= '月份')
	updateTime = models.DateTimeField(auto_now= True, verbose_name='更改日期')
	catIncome = models.FloatField(verbose_name= '猫收入')
	catOutcome = models.FloatField(verbose_name='猫支出')
	mouseIncome = models.FloatField(verbose_name='鼠收入')
	mouseOutcome = models.FloatField(verbose_name='鼠支出')
	specialIncome = models.CharField(max_length=500, verbose_name='共同收入', default='')
	specialOutcome = models.CharField(max_length=500, verbose_name='共同支出', default='')
	class Meta:
		db_table = 'db_summary'
		verbose_name = '财务小结'
		verbose_name_plural = '财务小结'
		constraints = [models.UniqueConstraint(fields=['year', 'month'], name='unique_period')]
		
		
class IncomeStatistic(models.Model):
	no = models.AutoField(primary_key=True, verbose_name='编号')
	year = models.IntegerField(verbose_name='年份', default=0)
	month = models.IntegerField(verbose_name='月份', default=0)
	member = models.ForeignKey(Animal, on_delete=models.PROTECT, to_field='name', verbose_name='成员3',related_name="收入统计")
	updateTime = models.DateTimeField(auto_now=True, verbose_name='更改日期')
	# 收入类型
	incomeFinance = models.FloatField(verbose_name='理财', default=0)
	incomeSalary = models.FloatField(verbose_name='工资', default=0)
	incomeReward = models.FloatField(verbose_name='奖金', default=0)
	incomeOther = models.CharField(max_length=200, verbose_name='额外收入', default='')
	
	class Meta:
		db_table = 'db_statistic_income'
		verbose_name = '财务统计(收入)'
		verbose_name_plural = '财务统计(收入)'


class OutcomeStatistic(models.Model):
	no = models.AutoField(primary_key=True, verbose_name='编号')
	year = models.IntegerField(verbose_name='年份', default=0)
	month = models.IntegerField(verbose_name='月份', default=0)
	member = models.ForeignKey(Animal, on_delete=models.PROTECT, to_field='name', verbose_name='成员2',related_name="支出统计")
	updateTime = models.DateTimeField(auto_now=True, verbose_name='更改日期')
	# 支出类型
	personalExpense = models.FloatField(verbose_name='月度个人支出', default=0)
	familyExpense = models.FloatField(verbose_name='月度家庭支出', default=0)
	outcomePerMeal = models.FloatField(verbose_name='独自用餐', default=0)
	outcomeTogMeal = models.FloatField(verbose_name='共同用餐', default=0)
	outcomeGame = models.FloatField(verbose_name='游戏', default=0)
	outcomeWork = models.FloatField(verbose_name='工作', default=0)
	outcomeFamTravel = models.FloatField(verbose_name='旅游', default=0)
	outcomePurchase = models.FloatField(verbose_name='购物', default=0)
	outcomeTraffic = models.FloatField(verbose_name='交通', default=0)
	outcomeFamCat = models.FloatField(verbose_name='趣多多', default=0)
	outcomeFamEle = models.FloatField(verbose_name='水电', default=0)
	outcomeFamGas = models.FloatField(verbose_name='煤气', default=0)
	outcomeFamPurchase = models.FloatField(verbose_name='家庭采购', default=0)
	outcomeOther = models.CharField(max_length=200, verbose_name='额外支出', default='')
	
	class Meta:
		db_table = 'db_statistic_outcome'
		verbose_name = '财务统计(支出)'
		verbose_name_plural = '财务统计(支出)'



class Detail(models.Model):
	no = models.AutoField(primary_key=True, verbose_name='编号')
	time = models.DateTimeField(default=timezone.now, verbose_name='日期')
	member = models.ForeignKey(Animal, on_delete=models.PROTECT, to_field='name', verbose_name='成员1',related_name="具体记录")
	financeType = models.CharField(max_length=20, choices=(('income', '收入'), ('outcome', '支出'),), verbose_name='收入/支出')
	foodType = models.ForeignKey(Type, on_delete=models.PROTECT, to_field='foodType', verbose_name='类型', default='')
	amount = models.FloatField(verbose_name='金额')
	comment = models.CharField(max_length=20, verbose_name='备注', default='')
	class Meta:
		db_table = 'db_details'
		verbose_name = '财务记录'
		verbose_name_plural = '财务记录'