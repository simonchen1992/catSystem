from django.contrib import admin

# Register your models here.

from finance.models import animal, summary, detail



class summaryAdmin(admin.ModelAdmin):
	list_display = ('year', 'month', 'member', 'financeType','amount')
	
class detailAdmin(admin.ModelAdmin):
	list_display = ('time', 'member', 'financeType','amount')

admin.site.register(animal)
admin.site.register(summary, summaryAdmin)
admin.site.register(detail, detailAdmin)