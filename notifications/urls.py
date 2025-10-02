from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('read-all/', views.read_all, name='read_all'),
    path('', views.list_notifications, name='list'),
]


