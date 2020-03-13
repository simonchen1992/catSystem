
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
    path('detail/add/', views.detailAdd),
    path('detail/', views.detailDisplay),
    path('animal/add/', views.animalAdd),
    path('animal/', views.animalDisplay),
    path('summary/', views.summaryDisplay),
]