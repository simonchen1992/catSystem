
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
]