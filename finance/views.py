# Create your views here.
# encoding: utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from functools import wraps
import json
from django.core.paginator import Paginator
from finance.models import Animal, Summary, Detail, Type, OutcomeStatistic, IncomeStatistic
from django.views.decorators.csrf import ensure_csrf_cookie
import django.utils.timezone as timezone
from django import forms
import datetime
from django.utils.timezone import make_aware
from django.db.models import Sum


def check_login(f):
	@wraps(f)
	def inner(request,*arg,**kwargs):
		if request.session.get('is_login'):
			return f(request,*arg,**kwargs)
		else:
			return redirect('/login/')
	return inner

#@check_login
@ensure_csrf_cookie
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

# def detailFilter(request):
# 	if request.method == 'GET':
# 		# if request.GET.get('hint'):
# 		# 	hint = request.GET.get('hint')
# 		# else:
# 		# 	hint = ''
# 		if request.GET.get('member', ''):
# 			details = Detail.objects.filter(member_id=request.GET.get('member', '')).order_by('-time')
# 		else:
# 			details = Detail.objects.order_by('-time')
# 		paginator = Paginator(details, 15)
# 		pageNum = request.GET.get('page', default='1')
# 		try:
# 			page = paginator.page(pageNum)
# 		except Exception as e:
# 			page = paginator.page(1)
# 			pageNum = 1
		
# 		# 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
# 		pageNum = int(pageNum)
# 		if pageNum < 6:
# 			if paginator.num_pages <= 10:
# 				displayRange = range(1, paginator.num_pages + 1)
# 			else:
# 				displayRange = range(1, 11)
# 		elif (pageNum >= 6) and (pageNum <= paginator.num_pages - 5):
# 			displayRange = range(pageNum - 5, pageNum + 5)
# 		else:
# 			displayRange = range(paginator.num_pages - 9, paginator.num_pages + 1)
# 		data = {'page': page, 'paginator': paginator, 'dis_range': displayRange}
# 	return render(request, 'detail.html', data)


def detailAdd(request):
	animals = Animal.objects.all()
	data = {'defaultMember': "猫哥",
			"defaultFinanceType": "支出",
			"defaultDateTime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M"),
			'animals': animals,
			'incomeType': Type.objects.filter(financeType='收入'),
			'outcomeType': Type.objects.filter(financeType='支出'),
			"duplicate": {"duplicate": False, "defaultAmount": "", "defaultFoodType": "", "defaultComment": "", "detail": ""},
			'hint': ""}
	if request.method == 'POST':
		data["defaultMember"] = request.POST['member_id']
		data["defaultFinanceType"] = request.POST['financeType']
		data["defaultDateTime"] = request.POST["datetime"]
		if request.POST and request.POST['member_id'] and request.POST['financeType'] and request.POST['amount'] and \
				request.POST['foodType'] and (
				request.POST['comment'] or request.POST['foodType'] not in ['额外支出', '额外收入']):
			# get datetime from frontend
			input_time = datetime.datetime.strptime(request.POST['datetime'], '%Y-%m-%dT%H:%M')
			# check if there's duplicate detail in database, double confirm with user
			duplicate_detail = Detail.objects.filter(member_id=request.POST['member_id'],
													 financeType=request.POST['financeType'],
													 amount=request.POST['amount'],
													 foodType_id=request.POST['foodType'])
			if duplicate_detail and ('duplicate_check' not in request.POST.keys() or request.POST["duplicate_check"] is True):
				data["duplicate"]["defaultAmount"] = request.POST['amount']
				data["duplicate"]["defaultFoodType"] = request.POST['foodType']
				data["duplicate"]["defaultComment"] = request.POST['comment']
				for du in duplicate_detail:
					if du.time.year == input_time.year and du.time.month == input_time.month and du.time.day == input_time.day:
						du.time += datetime.timedelta(hours=8)
						data["duplicate"]["duplicate"] = True
						data["duplicate"]["detail"] += "时间: %s,人物：%s, 金额: %s, 类型: %s, 备注: %s \\n " % (
						du.time, du.member, du.amount, du.foodType_id, du.comment)
				if data["duplicate"]["duplicate"]:
					return render(request, 'detailAdd.html', data)
			# record detail into database, time will always exist
			# input_time = datetime.datetime.strptime(request.POST['datetime'], '%Y-%m-%dT%H:%M')
			now = datetime.datetime.now()
			diff_time = now - input_time
			if diff_time.days < 0:
				data["hint"] = '不允许填入未来的时间！'
				return render(request, 'detailAdd.html', data)
			d = Detail(member_id=request.POST['member_id'], time=make_aware(input_time), financeType=request.POST['financeType'],
					   amount=request.POST['amount'], foodType_id=request.POST['foodType'],
					   comment=request.POST['comment'])
			d.save()
			data["hint"] = '成功录入粮食记录'
		else:
			data["hint"] = '戆都填完所有空格！'
	return render(request, 'detailAdd.html', data)


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
		summarys = Summary.objects.order_by('-year', '-month')
		
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
	update_package = [(curM, curY, detailCurMonth)]
	# update for one past year from now
	for i in range(11):
		if curM > 1:
			lastY = curY
			lastM = curM - 1
			detailLastMonth = Detail.objects.filter(time__year=lastY).filter(time__month=lastM)
		else:
			lastY = curY - 1
			lastM = 12
			detailLastMonth = Detail.objects.filter(time__year=lastY).filter(time__month=lastM)
		curM = lastM
		curY = lastY
		update_package.append((lastM, lastY, detailLastMonth))
	

	def calculate(d, member_id, type):
		result = 0
		if d.filter(member_id=member_id, financeType=type):
			for item in d.filter(member_id=member_id, financeType=type):
				result += item.amount
		return round(result, 2)
	
	# update last month and current month
	for (month, year, detail) in update_package:
		if Summary.objects.filter(year=year).filter(month=month):
			summary = Summary.objects.filter(year= year).filter(month=month)[0]
		else:
			summary = Summary(year=year, month=month)
		summary.catIncome = calculate(detail, '猫哥', '收入')
		summary.catOutcome = calculate(detail, '猫哥', '支出')
		summary.mouseIncome = calculate(detail, '鼠妹', '收入')
		summary.mouseOutcome = calculate(detail, '鼠妹', '支出')
		otherAnimal = Animal.objects.exclude(name__in=['猫哥', '鼠妹'])
		summary.specialIncome = ''
		summary.specialOutcome = ''
		for t in otherAnimal:
			summary.specialIncome += '%s: %.1f; ' % (t.name, calculate(detail, t.name, '收入'))
			summary.specialOutcome += '%s: %.1f; ' % (t.name, calculate(detail, t.name, '支出'))
		summary.save()


def statisticDisplay(request, financeType):
	if request.method == 'GET':
		statisticUpdate(financeType)
		if financeType == '收入':
			statistics = IncomeStatistic.objects.order_by('-year', '-month')
			# statistics = Detail.objects.filter(financeType="收入", foodType="奖金").values("member", "foodType", "time__year", "time__month").annotate(amount=Sum("amount"))
			# import pandas as pd
			# statistics = pd.DataFrame(statistics)
			# input(statistics)
		elif financeType == '支出':
			statistics = OutcomeStatistic.objects.order_by('-year', '-month')
		# new added for filter
		if request.GET.get('member', ''):
			statistics = statistics.filter(member_id=request.GET.get('member', '')).order_by('-year', '-month')
		# /new added for filter
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
		data = {'page': page, 'paginator': paginator, 'dis_range': displayRange, "period": ""}
	elif request.method == 'POST':
		start_year = int(request.POST['start_month'].split("-")[0])
		start_month = int(request.POST['start_month'].split("-")[1])
		end_year = int(request.POST['end_month'].split("-")[0])
		end_month = int(request.POST['end_month'].split("-")[1])
		if financeType == '收入':
			statistics = IncomeStatistic.objects.filter(year__gte=start_year, year__lte=end_year, month__gte=start_month, month__lte=end_month).values('member_id')\
				.annotate(incomeSalary=Sum("incomeSalary"), incomeReward=Sum("incomeReward"), incomeFinance=Sum("incomeFinance"), incomeOther=Sum("incomeOther"))
		elif financeType == '支出':
			statistics = OutcomeStatistic.objects.filter(year__gte=start_year, year__lte=end_year, month__gte=start_month, month__lte=end_month).values('member_id')\
				.annotate(personalExpense=Sum("personalExpense"), familyExpense=Sum("familyExpense"), outcomePerMeal=Sum("outcomePerMeal"), outcomeTogMeal=Sum("outcomeTogMeal")\
					, outcomeGame=Sum("outcomeGame"), outcomeWork=Sum("outcomeWork"), outcomeGift=Sum("outcomeGift"), outcomeTraffic=Sum("outcomeTraffic")\
						, outcomePurchase=Sum("outcomePurchase"), outcomeFamCat=Sum("outcomeFamCat"), outcomeFamEle=Sum("outcomeFamEle"), outcomeFamGas=Sum("outcomeFamGas")\
							, outcomeFamPurchase=Sum("outcomeFamPurchase"), outcomeFamTravel=Sum("outcomeFamTravel"), outcomeOther=Sum("outcomeOther"))
		paginator = Paginator(statistics, 15)
		page = paginator.page(1)
		data = {'page': page, 'paginator': paginator, 'dis_range': [1], "period": "{} - {}".format(request.POST['start_month'].replace("-", "."), request.POST['end_month'].replace("-", "."))}
	if financeType == '收入':
		return render(request, 'incomeSta.html', data)
	elif financeType == '支出':
		return render(request, 'outcomeSta.html', data)


def statisticUpdate(financeType):
	curY = datetime.date.today().year
	curM = datetime.date.today().month
	detailCurMonth = Detail.objects.filter(time__year=curY).filter(time__month=curM)
	update_package = [(curM, curY, detailCurMonth)]
	# update for one past year from now
	for i in range(2):
		if curM > 1:
			lastY = curY
			lastM = curM - 1
			detailLastMonth = Detail.objects.filter(time__year=lastY).filter(time__month=lastM)
		else:
			lastY = curY - 1
			lastM = 12
			detailLastMonth = Detail.objects.filter(time__year=lastY).filter(time__month=lastM)
		curM = lastM
		curY = lastY
		update_package.append((lastM, lastY, detailLastMonth))
	

	def calculate(d, member_id, financeType, foodType):
		result = 0
		if d.filter(member_id=member_id, financeType=financeType, foodType_id=foodType):
			for item in d.filter(member_id=member_id, financeType=financeType, foodType_id=foodType):
				result += item.amount
		return round(result, 2)

	# update last month and current month
	for (month, year, detail) in update_package:
		if financeType == '收入':
			for member_id in ['猫哥', '鼠妹']:
				if IncomeStatistic.objects.filter(year=year).filter(month=month).filter(member_id=member_id):
					sta = IncomeStatistic.objects.filter(year=year).filter(month=month).filter(member_id=member_id)[0]
				else:
					sta = IncomeStatistic(year=year, month=month, member_id=member_id)
				sta.member_id = member_id
				sta.incomeFinance = calculate(detail, member_id, financeType, '理财')
				sta.incomeSalary = calculate(detail, member_id, financeType, '工资')
				sta.incomeReward = calculate(detail, member_id, financeType, '奖金')
				# sta.incomeOther = ''
				# for t in detail.filter(member_id=member_id, financeType=financeType, foodType_id='额外收入'):
				# 	sta.incomeOther += '%s: %.1f; ' % (t.comment, t.amount)
				sta.incomeOther = calculate(detail, member_id, financeType, '额外收入')
				sta.save()
		elif financeType == '支出':
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
				sta.outcomeWork = calculate(detail, member_id, financeType, '工作')
				sta.outcomeGift = calculate(detail, member_id, financeType, '礼物')
				sta.outcomeFamTravel = calculate(detail, member_id, financeType, '旅游')
				sta.outcomePurchase = calculate(detail, member_id, financeType, '购物')
				sta.outcomeTraffic = calculate(detail, member_id, financeType, '交通')
				sta.outcomeFamCat = calculate(detail, member_id, financeType, '趣多多')
				sta.outcomeFamEle = calculate(detail, member_id, financeType, '水电')
				sta.outcomeFamGas = calculate(detail, member_id, financeType, '煤气')
				sta.outcomeFamPurchase = calculate(detail, member_id, financeType, '家庭采购')
				sta.personalExpense = round(sta.outcomePerMeal + sta.outcomeGame + sta.outcomeWork + sta.outcomeGift + sta.outcomePurchase + togMealCal + sta.outcomeTraffic, 2)
				sta.familyExpense = round(sta.outcomeFamCat + sta.outcomeFamEle + sta.outcomeFamGas + sta.outcomeFamTravel + sta.outcomeFamPurchase, 2)
				# sta.outcomeOther = ''
				# for t in detail.filter(member_id=member_id, financeType=financeType, foodType_id='额外支出'):
				# 	sta.outcomeOther += '%s: %.1f; ' % (t.comment, t.amount)
				sta.outcomeOther = calculate(detail, member_id, financeType, '额外支出')
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