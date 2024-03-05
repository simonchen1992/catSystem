
# from django.contrib import admin

#
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.urls import path
from django.urls import path

from finance import views

urlpatterns = [
    path('', views.index),
    path('index/', views.index),
    path('detail/add/', views.detail_add),
    path('detail/', views.detail_display),
    path('animal/add/', views.animal_add),
    path('animal/', views.animal_display),
    path('summary/', views.summary_display),
    path('statistic/income/', views.statistic_display, kwargs={'finance_type': '收入'}),
    path('statistic/outcome/', views.statistic_display, kwargs={'finance_type': '支出'})
    #path('statistic/(?P<year>\d+)/(?P<month>\d+)', views.statisticDisplay, name='statistic')
]