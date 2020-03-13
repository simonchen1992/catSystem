from django.contrib import admin

# Register your models here.

from finance.models import Animal, Summary, Detail



class summaryAdmin(admin.ModelAdmin):
	list_display = ('year', 'month',)
	
class detailAdmin(admin.ModelAdmin):
	list_display = ('time', 'financeType','amount')

admin.site.register(Animal)
admin.site.register(Summary, summaryAdmin)
admin.site.register(Detail, detailAdmin)