# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from functools import wraps
import json
from django.core.paginator import Paginator
from finance.models import Animal, Summary, Detail
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
		details = Detail.objects.all()
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
		data = {'page': page, 'paginator': paginator, 'dis_range': displayRange, 'cols': Detail.objects.values()[0].keys()}
		return render(request, 'detail.html', data)


def detailAdd(request):
	animals = Animal.objects.all()
	hint = ''
	if request.method == 'POST':
		if request.POST and request.POST['member_id'] and request.POST['financeType'] and request.POST['amount']:
			d = Detail(member_id = request.POST['member_id'], financeType = request.POST['financeType'], amount = request.POST['amount'])
			d.save()
			hint = '成功录入粮食记录'
		else:
			hint = '戆都填完所有空格！'
	return render(request, 'detailAdd.html', {'animals': animals, 'hint': hint})


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
		summarys = Summary.objects.all()
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
	if Summary.objects.filter(year=curY).filter(month=curM):
		summaryCurMonth = Summary.objects.filter(year=curY).filter(month=curM)[0]
	else:
		summaryCurMonth = Summary(year=curY, month=curM)
	summaryCurMonth.catIncome = calculate(detailCurMonth, '猫', 'income')
	summaryCurMonth.catOutcome = calculate(detailCurMonth, '猫', 'outcome')
	summaryCurMonth.mouseIncome = calculate(detailCurMonth, '鼠', 'income')
	summaryCurMonth.mouseOutcome = calculate(detailCurMonth, '鼠', 'outcome')
	otherAnimal = Animal.objects.exclude(name__in = ['猫', '鼠'])
	summaryCurMonth.specialIncome = ''
	summaryCurMonth.specialOutcome = ''
	for t in otherAnimal:
		summaryCurMonth.specialIncome += '%s: %.1f; ' %(t.name, calculate(detailCurMonth, t.name, 'income'))
		summaryCurMonth.specialOutcome += '%s: %.1f; ' % (t.name, calculate(detailCurMonth, t.name, 'outcome'))
	summaryCurMonth.save()
	
	
	if Summary.objects.filter(year= lastY).filter(month= lastM):
		summaryLastMonth = Summary.objects.filter(year= lastY).filter(month=lastM)[0]
	else:
		summaryLastMonth = Summary(year=lastY, month=lastM)
	summaryLastMonth.catIncome = calculate(detailLastMonth, '猫', 'income')
	summaryLastMonth.catOutcome = calculate(detailLastMonth, '猫', 'outcome')
	summaryLastMonth.mouseIncome = calculate(detailLastMonth, '鼠', 'income')
	summaryLastMonth.mouseOutcome = calculate(detailLastMonth, '鼠', 'outcome')
	otherAnimal = Animal.objects.exclude(name__in=['猫', '鼠'])
	summaryLastMonth.specialIncome = ''
	summaryLastMonth.specialOutcome = ''
	for t in otherAnimal:
		summaryLastMonth.specialIncome += '%s: %.1f; ' % (t.name, calculate(detailLastMonth, t.name, 'income'))
		summaryLastMonth.specialOutcome += '%s: %.1f; ' % (t.name, calculate(detailLastMonth, t.name, 'outcome'))
	summaryLastMonth.save()

def index(request):
	return render(request, 'index.html')