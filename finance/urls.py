
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
    # path('detail/filter/', views.detailFilter),
    path('detail/add/', views.detailAdd),
    path('detail/', views.detailDisplay),
    path('animal/add/', views.animalAdd),
    path('animal/', views.animalDisplay),
    path('summary/', views.summaryDisplay),
    path('statistic/income/', views.statisticDisplay, kwargs={'financeType': '收入'}),
    path('statistic/outcome/', views.statisticDisplay, kwargs={'financeType': '支出'})
    #path('statistic/(?P<year>\d+)/(?P<month>\d+)', views.statisticDisplay, name='statistic')
]