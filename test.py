from finance.models import Animal, Summary, Detail, Type, OutcomeStatistic, IncomeStatistic

update_list = [("收入", "派派红包"), ("支出", "派派"), ("支出", "医疗")]
for item in update_list:
    # search
    if not Type.objects.filter(financeType=item[0], foodType=item[1]):
        # add
        t = Type(financeType=item[0], foodType=item[1])
        t.save()

# # delete
# Type.objects.filter(financeType=item[0], foodType=item[1]).delete()
# # update
# # todo
