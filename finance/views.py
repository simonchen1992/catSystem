# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from functools import wraps
import json
from django.core.paginator import Paginator
from finance.models import Animal, Summary, Detail, Type, OutcomeStatistic, IncomeStatistic
import django.utils.timezone as timezone
from django import forms
import datetime



def check_login(f):
	@wraps(f)
	def inner(request,*arg,**kwargs):
		if request.session.get('is_login'):
			return f(request,*arg,**kwargs)
		else:
			return redirect('/login/')
	return inner

#@check_login
def detailDisplay(request):
	if request.method == 'GET':
		# if request.GET.get('hint'):
		# 	hint = request.GET.get('hint')
		# else:
		# 	hint = ''
		details = Detail.objects.order_by('-time')
		if request.GET.get('member', ''):
			details = details.filter(member_id=request.GET.get('member', '')).order_by('-time')
		if request.GET.get('financeType', ''):
			details = details.filter(financeType=request.GET.get('financeType', '')).order_by('-time')
		if request.GET.get('foodType', ''):
			details = details.filter(foodType=request.GET.get('foodType', '')).order_by('-time')
		paginator = Paginator(details, 15)
		pageNum = request.GET.get('page', default='1')
		try:
			page = paginator.page(pageNum)
		except Exception as e:
			page = paginator.page(1)
			pageNum = 1
		
		# 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
		pageNum = int(pageNum)
		if pageNum < 6:
			if paginator.num_pages <= 10:
				displayRange = range(1, paginator.num_pages + 1)
			else:
				displayRange = range(1, 11)
		elif (pageNum >= 6) and (pageNum <= paginator.num_pages - 5):
			displayRange = range(pageNum - 5, pageNum + 5)
		else:
			displayRange = range(paginator.num_pages - 9, paginator.num_pages + 1)
		data = {'page': page, 'paginator': paginator, 'dis_range': displayRange}
		return render(request, 'detail.html', data)
	if request.method == 'POST':
		delete_id = request.POST['delete_id']
		password = request.POST['password']
		if password == 'HJH930712':
			Detail.objects.filter(pk=delete_id).delete()
			return HttpResponse('Delete record successfully.')
		else:
			return HttpResponse('Wrong password!')

def detailFilter(request):
	if request.method == 'GET':
		# if request.GET.get('hint'):
		# 	hint = request.GET.get('hint')
		# else:
		# 	hint = ''
		if request.GET.get('member', ''):
			details = Detail.objects.filter(member_id=request.GET.get('member', '')).order_by('-time')
		else:
			details = Detail.objects.order_by('-time')
		paginator = Paginator(details, 15)
		pageNum = request.GET.get('page', default='1')
		try:
			page = paginator.page(pageNum)
		except Exception as e:
			page = paginator.page(1)
			pageNum = 1
		
		# 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
		pageNum = int(pageNum)
		if pageNum < 6:
			if paginator.num_pages <= 10:
				displayRange = range(1, paginator.num_pages + 1)
			else:
				displayRange = range(1, 11)
		elif (pageNum >= 6) and (pageNum <= paginator.num_pages - 5):
			displayRange = range(pageNum - 5, pageNum + 5)
		else:
			displayRange = range(paginator.num_pages - 9, paginator.num_pages + 1)
		data = {'page': page, 'paginator': paginator, 'dis_range': displayRange}
	return render(request, 'summary.html', data)

def detailAdd(request):
	animals = Animal.objects.all()
	incomeType = Type.objects.filter(financeType = '收入')
	outcomeType = Type.objects.filter(financeType = '支出')
	hint = ''
	if request.method == 'POST':
		if request.POST and request.POST['member_id'] and request.POST['financeType'] and request.POST['amount'] and request.POST['foodType'] and (request.POST['comment'] or request.POST['foodType'] not in ['额外支出', '额外收入']):
			if request.POST['datetime'] == '':
				d = Detail(member_id = request.POST['member_id'], financeType = request.POST['financeType'], amount = request.POST['amount'], foodType_id=request.POST['foodType'], comment=request.POST['comment'])
			else:
				fixTime = datetime.datetime.strptime(request.POST['datetime'], '%Y-%m-%dT%H:%M')
				now = datetime.datetime.now()
				diffTime = now - fixTime
				if diffTime.days < 0:
					hint = '不允许填入未来的时间！'
					return render(request, 'detailAdd.html', {'animals': animals, 'incomeType': incomeType, 'outcomeType': outcomeType, 'hint': hint})
				d = Detail(member_id=request.POST['member_id'], time=fixTime, financeType = request.POST['financeType'], amount = request.POST['amount'], foodType_id=request.POST['foodType'], comment=request.POST['comment'])
			d.save()
			hint = '成功录入粮食记录'
		else:
			hint = '戆都填完所有空格！'
	return render(request, 'detailAdd.html', {'animals': animals, 'incomeType': incomeType, 'outcomeType': outcomeType, 'hint': hint})

	


def animalDisplay(request):
	if request.method == 'GET':
		animals = Animal.objects.all()
		paginator = Paginator(animals, 15)
		pageNum = request.GET.get('page', default='1')
		try:
			page = paginator.page(pageNum)
		except Exception as e:
			page = paginator.page(1)
			pageNum = 1
		
		# 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
		pageNum = int(pageNum)
		if pageNum < 6:
			if paginator.num_pages <= 10:
				displayRange = range(1, paginator.num_pages + 1)
			else:
				displayRange = range(1, 11)
		elif (pageNum >= 6) and (pageNum <= paginator.num_pages - 5):
			displayRange = range(pageNum - 5, pageNum + 5)
		else:
			displayRange = range(paginator.num_pages - 9, paginator.num_pages + 1)
		# cols = Detail.objects.values()[0].keys() # get field name of database
		data = {'page': page, 'paginator': paginator, 'dis_range': displayRange}
		return render(request, 'animal.html', data)


def animalAdd(request):
	hint = ''
	if request.method == 'POST':
		if request.POST and request.POST['name']:
			a = Animal(name=request.POST['name'])
			a.save()
			hint = '成功录入动物成员'
		else:
			hint = '戆都填完所有空格！'
	return render(request, 'animalAdd.html', {'hint': hint})


def summaryDisplay(request):
	if request.method == 'GET':
		summaryUpdate()
		summarys = Summary.objects.order_by('-month')
		
		paginator = Paginator(summarys, 15)
		pageNum = request.GET.get('page', default='1')
		try:
			page = paginator.page(pageNum)
		except Exception as e:
			page = paginator.page(1)
			pageNum = 1
		
		# 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
		pageNum = int(pageNum)
		if pageNum < 6:
			if paginator.num_pages <= 10:
				displayRange = range(1, paginator.num_pages + 1)
			else:
				displayRange = range(1, 11)
		elif (pageNum >= 6) and (pageNum <= paginator.num_pages - 5):
			displayRange = range(pageNum - 5, pageNum + 5)
		else:
			displayRange = range(paginator.num_pages - 9, paginator.num_pages + 1)
		# cols = detail.objects.values()[0].keys() # get field name of database
		data = {'page': page, 'paginator': paginator, 'dis_range': displayRange}
		return render(request, 'summary.html', data)


def summaryUpdate():
	curY =datetime.date.today().year
	curM = datetime.date.today().month
	detailCurMonth = Detail.objects.filter(time__year= curY).filter(time__month= curM)
	if datetime.date.today().month > 1:
		lastY = datetime.date.today().year
		lastM = datetime.date.today().month - 1
		detailLastMonth = Detail.objects.filter(time__year= lastY).filter(time__month= lastM)
	else:
		lastY = datetime.date.today().year - 1
		lastM = 12
		detailLastMonth = Detail.objects.filter(time__year=lastY).filter(time__month= lastM)
	
	def calculate(d, member_id, type):
		result = 0
		if d.filter(member_id = member_id, financeType = type):
			for item in d.filter(member_id = member_id, financeType = type):
				result += item.amount
		return result
	
	# update last month and current month
	for (month, year, detail) in [(lastM, lastY, detailLastMonth), (curM, curY, detailCurMonth)]:
		if Summary.objects.filter(year= year).filter(month= month):
			summary = Summary.objects.filter(year= year).filter(month=month)[0]
		else:
			summary = Summary(year=year, month=month)
		summary.catIncome = calculate(detail, '猫哥', 'income')
		summary.catOutcome = calculate(detail, '猫哥', 'outcome')
		summary.mouseIncome = calculate(detail, '鼠妹', 'income')
		summary.mouseOutcome = calculate(detail, '鼠妹', 'outcome')
		otherAnimal = Animal.objects.exclude(name__in=['猫哥', '鼠妹'])
		summary.specialIncome = ''
		summary.specialOutcome = ''
		for t in otherAnimal:
			summary.specialIncome += '%s: %.1f; ' % (t.name, calculate(detail, t.name, 'income'))
			summary.specialOutcome += '%s: %.1f; ' % (t.name, calculate(detail, t.name, 'outcome'))
		summary.save()


def statisticDisplay(request, financeType):
	if request.method == 'GET':
		statisticUpdate(financeType)
		if financeType == 'income':
			statistics = IncomeStatistic.objects.order_by('-month')
			#statistics = IncomeStatistic.objects.all()
		elif financeType == 'outcome':
			statistics = OutcomeStatistic.objects.order_by('-month')
		paginator = Paginator(statistics, 15)
		pageNum = request.GET.get('page', default='1')
		try:
			page = paginator.page(pageNum)
		except Exception as e:
			page = paginator.page(1)
			pageNum = 1

		# 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
		pageNum = int(pageNum)
		if pageNum < 6:
			if paginator.num_pages <= 10:
				displayRange = range(1, paginator.num_pages + 1)
			else:
				displayRange = range(1, 11)
		elif (pageNum >= 6) and (pageNum <= paginator.num_pages - 5):
			displayRange = range(pageNum - 5, pageNum + 5)
		else:
			displayRange = range(paginator.num_pages - 9, paginator.num_pages + 1)
		# cols = detail.objects.values()[0].keys() # get field name of database
		data = {'page': page, 'paginator': paginator, 'dis_range': displayRange}
		if financeType == 'income':
			return render(request, 'incomeSta.html', data)
		elif financeType == 'outcome':
			return render(request, 'outcomeSta.html', data)


def statisticUpdate(financeType):
	curY = datetime.date.today().year
	curM = datetime.date.today().month
	detailCurMonth = Detail.objects.filter(time__year=curY).filter(time__month=curM)
	if datetime.date.today().month > 1:
		lastY = datetime.date.today().year
		lastM = datetime.date.today().month - 1
		detailLastMonth = Detail.objects.filter(time__year=lastY).filter(time__month=lastM)
	else:
		lastY = datetime.date.today().year - 1
		lastM = 12
		detailLastMonth = Detail.objects.filter(time__year=lastY).filter(time__month=lastM)

	def calculate(d, member_id, financeType, foodType):
		result = 0
		if d.filter(member_id=member_id, financeType=financeType, foodType_id=foodType):
			for item in d.filter(member_id=member_id, financeType=financeType, foodType_id=foodType):
				result += item.amount
		return round(result, 2)

	# update last month and current month
	for (month, year, detail) in [(lastM, lastY, detailLastMonth), (curM, curY, detailCurMonth)]:
		if financeType == 'income':
			for member_id in ['猫哥', '鼠妹']:
				if IncomeStatistic.objects.filter(year=year).filter(month=month).filter(member_id=member_id):
					sta = IncomeStatistic.objects.filter(year=year).filter(month=month).filter(member_id=member_id)[0]
				else:
					sta = IncomeStatistic(year=year, month=month, member_id=member_id)
				sta.member_id = member_id
				sta.incomeFinance = calculate(detail, member_id, financeType, '理财')
				sta.incomeSalary = calculate(detail, member_id, financeType, '工资')
				sta.incomeReward = calculate(detail, member_id, financeType, '奖金')
				sta.incomeOther = ''
				for t in detail.filter(member_id=member_id, financeType=financeType, foodType_id='额外收入'):
					sta.incomeOther += '%s: %.1f; ' % (t.comment, t.amount)
				sta.save()
		elif financeType == 'outcome':
			for member_id in ['猫哥', '鼠妹']:
				if OutcomeStatistic.objects.filter(year=year).filter(month=month).filter(member_id=member_id):
					sta = OutcomeStatistic.objects.filter(year=year).filter(month=month).filter(member_id=member_id)[0]
				else:
					sta = OutcomeStatistic(year=year, month=month, member_id=member_id)
				sta.member_id = member_id
				sta.outcomePerMeal = calculate(detail, member_id, financeType, '独自用餐')
				sta.outcomeTogMeal = calculate(detail, member_id, financeType, '共同用餐')
				togMealCal = (calculate(detail, '猫哥', financeType, '共同用餐') + calculate(detail, '鼠妹', financeType, '共同用餐'))/2
				sta.outcomeGame = calculate(detail, member_id, financeType, '游戏')
				sta.outcomeFamTravel = calculate(detail, member_id, financeType, '旅游')
				sta.outcomePurchase = calculate(detail, member_id, financeType, '购物')
				sta.outcomeTraffic = calculate(detail, member_id, financeType, '交通')
				sta.outcomeFamCat = calculate(detail, member_id, financeType, '趣多多')
				sta.outcomeFamEle = calculate(detail, member_id, financeType, '水电')
				sta.outcomeFamGas = calculate(detail, member_id, financeType, '煤气')
				sta.outcomeFamPurchase = calculate(detail, member_id, financeType, '家庭采购')
				sta.personalExpense = round(sta.outcomePerMeal + sta.outcomeGame + sta.outcomePurchase + togMealCal + sta.outcomeTraffic, 2)
				sta.familyExpense = round(sta.outcomeFamCat + sta.outcomeFamEle + sta.outcomeFamGas + sta.outcomeFamTravel + sta.outcomeFamPurchase, 2)
				sta.outcomeOther = ''
				for t in detail.filter(member_id=member_id, financeType=financeType, foodType_id='额外支出'):
					sta.outcomeOther += '%s: %.1f; ' % (t.comment, t.amount)
				sta.save()

	# update current month
	# if financeType == 'outcome':
	# 	for member_id in ['猫哥', '鼠妹']:
	# 	if Summary.objects.filter(year=curY).filter(month=curM):
	# 		summaryCurMonth = Summary.objects.filter(year=curY).filter(month=curM)[0]
	# 	else:
	# 		summaryCurMonth = Summary(year=curY, month=curM)
	# 	summaryCurMonth.catIncome = calculate(detailCurMonth, '猫', 'income')
	# 	summaryCurMonth.catOutcome = calculate(detailCurMonth, '猫', 'outcome')
	# 	summaryCurMonth.mouseIncome = calculate(detailCurMonth, '鼠', 'income')
	# 	summaryCurMonth.mouseOutcome = calculate(detailCurMonth, '鼠', 'outcome')
	# 	otherAnimal = Animal.objects.exclude(name__in=['猫', '鼠'])
	# 	summaryCurMonth.specialIncome = ''
	# 	summaryCurMonth.specialOutcome = ''
	# 	for t in otherAnimal:
	# 		summaryCurMonth.specialIncome += '%s: %.1f; ' % (t.name, calculate(detailCurMonth, t.name, 'income'))
	# 		summaryCurMonth.specialOutcome += '%s: %.1f; ' % (t.name, calculate(detailCurMonth, t.name, 'outcome'))
	# 	summaryCurMonth.save()


def index(request):
	return render(request, 'index.html')