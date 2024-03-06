# Create your views here.
# encoding: utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.timezone import make_aware
from django.db.models import Sum
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.paginator import Paginator
# from django import forms
from functools import wraps
from finance.models import Animal, Summary, Detail, Type, OutcomeStatistic, IncomeStatistic
import datetime


def check_login(f):
    @wraps(f)
    def inner(request, *arg, **kwargs):
        if request.session.get('is_login'):
            return f(request, *arg, **kwargs)
        else:
            return redirect('/login/')

    return inner


def animal_display(request):
    if request.method == 'GET':
        animals = Animal.objects.all()
        # 页码GUI
        paginator = Paginator(animals, 15)
        page_num = int(request.GET.get('page', default='1'))
        page = paginator.page(page_num)
        # 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
        if page_num < 6:
            if paginator.num_pages <= 10:
                display_range = range(1, paginator.num_pages + 1)
            else:
                display_range = range(1, 11)
        elif (page_num >= 6) and (page_num <= paginator.num_pages - 5):
            display_range = range(page_num - 5, page_num + 5)
        else:
            display_range = range(paginator.num_pages - 9, paginator.num_pages + 1)
        # cols = Detail.objects.values()[0].keys() # get field name of database
        data = {'page': page, 'paginator': paginator, 'dis_range': display_range}
        return render(request, 'animal.html', data)


def animal_add(request):
    hint = ''
    if request.method == 'POST':
        if request.POST and request.POST['name']:
            a = Animal(name=request.POST['name'])
            a.save()
            hint = '成功录入动物成员'
        else:
            hint = '戆都填完所有空格！'
    return render(request, 'animalAdd.html', {'hint': hint})


# @check_login
@ensure_csrf_cookie
def detail_display(request):
    if request.method == 'GET':
        # if request.GET.get('hint'):
        # 	hint = request.GET.get('hint')
        # else:
        # 	hint = ''
        details = Detail.objects.order_by('-time')
        if request.GET.get('member', ''):
            details = details.filter(member=request.GET.get('member', '')).order_by('-time')
        if request.GET.get('financeType', ''):
            details = details.filter(financeType=request.GET.get('financeType', '')).order_by('-time')
        if request.GET.get('foodType', ''):
            details = details.filter(foodType=request.GET.get('foodType', '')).order_by('-time')
        # 页码GUI
        paginator = Paginator(details, 15)
        page_num = int(request.GET.get('page', default='1'))
        page = paginator.page(page_num)
        # 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
        if page_num < 6:
            if paginator.num_pages <= 10:
                display_range = range(1, paginator.num_pages + 1)
            else:
                display_range = range(1, 11)
        elif (page_num >= 6) and (page_num <= paginator.num_pages - 5):
            display_range = range(page_num - 5, page_num + 5)
        else:
            display_range = range(paginator.num_pages - 9, paginator.num_pages + 1)
        data = {'page': page, 'paginator': paginator, 'dis_range': display_range}
        return render(request, 'detail.html', data)
    elif request.method == 'POST':
        details = Detail.objects.order_by('-time')
        delete_id = request.POST['delete_id']
        password = request.POST['password']
        if password == 'HJH930712':
            details.filter(pk=delete_id).delete()
            return HttpResponse('Delete record successfully.')
        else:
            return HttpResponse('Wrong password!')


def detail_add(request):
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
        data["defaultMember"] = request.POST['member']
        data["defaultFinanceType"] = request.POST['financeType']
        data["defaultDateTime"] = request.POST["datetime"]
        if request.POST and request.POST['member'] and request.POST['financeType'] and request.POST['amount'] and \
                request.POST['foodType'] and (
                request.POST['comment'] or request.POST['foodType'] not in ['额外支出', '额外收入']):
            # get datetime from frontend
            input_time = datetime.datetime.strptime(request.POST['datetime'], '%Y-%m-%dT%H:%M')
            # check if there's duplicate detail in database, double confirm with user
            duplicate_detail = Detail.objects.filter(member=request.POST['member'],
                                                     financeType=request.POST['financeType'],
                                                     amount=request.POST['amount'],
                                                     foodType=request.POST['foodType'])
            if duplicate_detail and ('duplicate_check' not in request.POST.keys() or request.POST["duplicate_check"] is True):
                data["duplicate"]["defaultAmount"] = request.POST['amount']
                data["duplicate"]["defaultFoodType"] = request.POST['foodType']
                data["duplicate"]["defaultComment"] = request.POST['comment']
                for du in duplicate_detail:
                    if du.time.year == input_time.year and du.time.month == input_time.month and du.time.day == input_time.day:
                        du.time += datetime.timedelta(hours=8)
                        data["duplicate"]["duplicate"] = True
                        data["duplicate"]["detail"] += "时间: %s,人物：%s, 金额: %s, 类型: %s, 备注: %s \\n " % (
                            du.time, du.member, du.amount, du.foodType, du.comment)
                if data["duplicate"]["duplicate"]:
                    return render(request, 'detailAdd.html', data)
            # record detail into database, time will always exist
            # input_time = datetime.datetime.strptime(request.POST['datetime'], '%Y-%m-%dT%H:%M')
            now = datetime.datetime.now()
            diff_time = now - input_time
            if diff_time.days < 0:
                data["hint"] = '不允许填入未来的时间！'
                return render(request, 'detailAdd.html', data)
            # 创建数据库条目时如果有引用外键，需要在关键字增加_id，否则参数要求为实例对象
            d = Detail(member_id=request.POST['member'], time=make_aware(input_time), financeType=request.POST['financeType'],
                       amount=request.POST['amount'], foodType_id=request.POST['foodType'],
                       comment=request.POST['comment'])
            d.save()
            data["hint"] = '成功录入粮食记录'
        else:
            data["hint"] = '戆都填完所有空格！'
    return render(request, 'detailAdd.html', data)


def summary_display(request):
    if request.method == 'GET':
        summary_update()
        summaries = Summary.objects.order_by('-year', '-month')
        # 页码GUI
        paginator = Paginator(summaries, 15)
        page_num = int(request.GET.get('page', default='1'))
        page = paginator.page(page_num)
        # 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
        if page_num < 6:
            if paginator.num_pages <= 10:
                display_range = range(1, paginator.num_pages + 1)
            else:
                display_range = range(1, 11)
        elif (page_num >= 6) and (page_num <= paginator.num_pages - 5):
            display_range = range(page_num - 5, page_num + 5)
        else:
            display_range = range(paginator.num_pages - 9, paginator.num_pages + 1)
        # cols = detail.objects.values()[0].keys() # get field name of database
        data = {'page': page, 'paginator': paginator, 'dis_range': display_range}
        return render(request, 'summary.html', data)


def get_update_package():
    current_year = datetime.date.today().year
    current_month = datetime.date.today().month
    detail_cur_month = Detail.objects.filter(time__year=current_year).filter(time__month=current_month)
    update_package = [(current_month, current_year, detail_cur_month)]
    # update for one past year from now
    for i in range(11):
        if current_month > 1:
            current_month = current_month - 1
            detail_cur_month = Detail.objects.filter(time__year=current_year).filter(time__month=current_month)
        else:
            current_year = current_year - 1
            current_month = 12
            detail_cur_month = Detail.objects.filter(time__year=current_year).filter(time__month=current_month)
        update_package.append((current_month, current_year, detail_cur_month))
    return update_package


def calculate(details, member, finance_type, food_type=None):
    result = 0
    if food_type:
        filtered_details = details.filter(member=member, financeType=finance_type, foodType=food_type)
    else:
        filtered_details = details.filter(member=member, financeType=finance_type)
    for item in filtered_details:
        result += item.amount
    return round(result, 2)


def summary_update():
    update_package = get_update_package()
    for (month, year, detail) in update_package:
        if Summary.objects.filter(year=year).filter(month=month):
            summary = Summary.objects.filter(year=year).filter(month=month)[0]
        else:
            summary = Summary(year=year, month=month)
        summary.catIncome = calculate(detail, '猫哥', '收入')
        summary.catOutcome = calculate(detail, '猫哥', '支出')
        summary.mouseIncome = calculate(detail, '鼠妹', '收入')
        summary.mouseOutcome = calculate(detail, '鼠妹', '支出')
        other_animal = Animal.objects.exclude(name__in=['猫哥', '鼠妹'])
        summary.specialIncome = ''
        summary.specialOutcome = ''
        for t in other_animal:
            summary.specialIncome += '%s: %.1f; ' % (t.name, calculate(detail, t.name, '收入'))
            summary.specialOutcome += '%s: %.1f; ' % (t.name, calculate(detail, t.name, '支出'))
        summary.save()


def statistic_display(request, finance_type):
    data = {}
    if request.method == 'GET':
        statistic_update(finance_type)
        if finance_type == '收入':
            statistics = IncomeStatistic.objects.order_by('-year', '-month')
            # statistics = Detail.objects.filter(financeType="收入", foodType="奖金").values("member", "foodType", "time__year", "time__month").annotate(amount=Sum("amount"))
        elif finance_type == '支出':
            statistics = OutcomeStatistic.objects.order_by('-year', '-month')
        # new added for filter
        if request.GET.get('member', ''):
            statistics = statistics.filter(member=request.GET.get('member', '')).order_by('-year', '-month')
        # /new added for filter
        # 页码GUI
        paginator = Paginator(statistics, 15)
        page_num = int(request.GET.get('page', default='1'))
        page = paginator.page(page_num)
        # 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
        if page_num < 6:
            if paginator.num_pages <= 10:
                display_range = range(1, paginator.num_pages + 1)
            else:
                display_range = range(1, 11)
        elif (page_num >= 6) and (page_num <= paginator.num_pages - 5):
            display_range = range(page_num - 5, page_num + 5)
        else:
            display_range = range(paginator.num_pages - 9, paginator.num_pages + 1)
        # cols = detail.objects.values()[0].keys() # get field name of database
        data = {'page': page, 'paginator': paginator, 'dis_range': display_range, "period": ""}
    elif request.method == 'POST':
        start_year = int(request.POST['start_month'].split("-")[0])
        start_month = int(request.POST['start_month'].split("-")[1])
        end_year = int(request.POST['end_month'].split("-")[0])
        end_month = int(request.POST['end_month'].split("-")[1])
        # get filter date range set
        date_filter = []
        for year in range(start_year, end_year + 1):
            if start_year != end_year:
                if year == start_year:
                    date_filter.append((year, start_month, 12))
                elif year == end_year:
                    date_filter.append((year, 1, end_month))
                else:
                    date_filter.append((year, 1, 12))
            else:
                date_filter.append((year, start_month, end_month))
        statistics = None
        if finance_type == '收入':
            for date in date_filter:
                if not statistics:
                    statistics = IncomeStatistic.objects.filter(year=date[0], month__gte=date[1], month__lte=date[2])
                else:
                    statistics = statistics | IncomeStatistic.objects.filter(year=date[0], month__gte=date[1], month__lte=date[2])
            statistics = statistics.values('member').annotate(incomeSalary=Sum("incomeSalary"), incomeReward=Sum("incomeReward"), incomeFinance=Sum("incomeFinance"), incomeBaby=Sum("incomeBaby"), incomeOther=Sum("incomeOther"))
        elif finance_type == '支出':
            for date in date_filter:
                if not statistics:
                    statistics = OutcomeStatistic.objects.filter(year=date[0], month__gte=date[1], month__lte=date[2])
                else:
                    statistics = statistics | OutcomeStatistic.objects.filter(year=date[0], month__gte=date[1], month__lte=date[2])
            statistics = statistics.values('member').annotate(personalExpense=Sum("personalExpense"), familyExpense=Sum("familyExpense"), outcomePerMeal=Sum("outcomePerMeal"), outcomeTogMeal=Sum("outcomeTogMeal")
                                                              , outcomeGame=Sum("outcomeGame"), outcomeWork=Sum("outcomeWork"), outcomeGift=Sum("outcomeGift"), outcomeTraffic=Sum("outcomeTraffic")
                                                              , outcomePurchase=Sum("outcomePurchase"), outcomeFamCat=Sum("outcomeFamCat"), outcomeFamEle=Sum("outcomeFamEle"), outcomeFamGas=Sum("outcomeFamGas")
                                                              , outcomeFamBaby=Sum("outcomeFamBaby"), outcomeMedical=Sum("outcomeMedical"), outcomeFamPurchase=Sum("outcomeFamPurchase"), outcomeFamTravel=Sum("outcomeFamTravel"), outcomeOther=Sum("outcomeOther"))
        paginator = Paginator(statistics, 15)
        page = paginator.page(1)
        data = {'page': page, 'paginator': paginator, 'dis_range': [1], "period": "{} - {}".format(request.POST['start_month'].replace("-", "."), request.POST['end_month'].replace("-", "."))}
    if finance_type == '收入':
        return render(request, 'incomeSta.html', data)
    elif finance_type == '支出':
        return render(request, 'outcomeSta.html', data)


def statistic_update(finance_type):
    update_package = get_update_package()
    for (month, year, detail) in update_package:
        if finance_type == '收入':
            for member in ['猫哥', '鼠妹']:
                if IncomeStatistic.objects.filter(year=year).filter(month=month).filter(member=member):
                    sta = IncomeStatistic.objects.filter(year=year).filter(month=month).filter(member=member)[0]
                else:
                    # 创建数据库条目时如果有引用外键，需要在关键字增加_id，否则参数要求为实例对象
                    sta = IncomeStatistic(year=year, month=month, member_id=member)
                sta.incomeFinance = calculate(detail, member, finance_type, '理财')
                sta.incomeSalary = calculate(detail, member, finance_type, '工资')
                sta.incomeReward = calculate(detail, member, finance_type, '奖金')
                sta.incomeBaby = calculate(detail, member, finance_type, '派派红包')
                # sta.incomeOther = ''
                # for t in detail.filter(member=member, financeType=financeType, foodType='额外收入'):
                # 	sta.incomeOther += '%s: %.1f; ' % (t.comment, t.amount)
                sta.incomeOther = calculate(detail, member, finance_type, '额外收入')
                sta.save()
        elif finance_type == '支出':
            for member in ['猫哥', '鼠妹']:
                if OutcomeStatistic.objects.filter(year=year).filter(month=month).filter(member=member):
                    sta = OutcomeStatistic.objects.filter(year=year).filter(month=month).filter(member=member)[0]
                else:
                    # 创建数据库条目时如果有引用外键，需要在关键字增加_id，否则参数要求为实例对象
                    sta = OutcomeStatistic(year=year, month=month, member_id=member)
                sta.outcomePerMeal = calculate(detail, member, finance_type, '独自用餐')
                sta.outcomeTogMeal = calculate(detail, member, finance_type, '共同用餐')
                tog_meal_cal = (calculate(detail, '猫哥', finance_type, '共同用餐') + calculate(detail, '鼠妹', finance_type, '共同用餐')) / 2
                sta.outcomeGame = calculate(detail, member, finance_type, '游戏')
                sta.outcomeWork = calculate(detail, member, finance_type, '工作')
                sta.outcomeGift = calculate(detail, member, finance_type, '礼物')
                sta.outcomeTraffic = calculate(detail, member, finance_type, '交通')
                sta.outcomePurchase = calculate(detail, member, finance_type, '购物')
                sta.outcomeMedical = calculate(detail, member, finance_type, '医疗')
                sta.outcomeFamBaby = calculate(detail, member, finance_type, '派派')
                sta.outcomeFamCat = calculate(detail, member, finance_type, '趣多多')
                sta.outcomeFamEle = calculate(detail, member, finance_type, '水电')
                sta.outcomeFamGas = calculate(detail, member, finance_type, '煤气')
                sta.outcomeFamPurchase = calculate(detail, member, finance_type, '家庭采购')
                sta.outcomeFamTravel = calculate(detail, member, finance_type, '旅游')
                sta.personalExpense = round(sta.outcomeMedical + sta.outcomePerMeal + sta.outcomeGame + sta.outcomeWork + sta.outcomeGift + sta.outcomePurchase + tog_meal_cal + sta.outcomeTraffic, 2)
                sta.familyExpense = round(sta.outcomeFamBaby + sta.outcomeFamCat + sta.outcomeFamEle + sta.outcomeFamGas + sta.outcomeFamTravel + sta.outcomeFamPurchase, 2)
                # sta.outcomeOther = ''
                # for t in detail.filter(member=member, financeType=financeType, foodType='额外支出'):
                # 	sta.outcomeOther += '%s: %.1f; ' % (t.comment, t.amount)
                sta.outcomeOther = calculate(detail, member, finance_type, '额外支出')
                sta.save()


# update current month
# if financeType == 'outcome':
# 	for member in ['猫哥', '鼠妹']:
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
