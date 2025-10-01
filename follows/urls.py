from django.urls import path
from . import views

app_name = 'follows'

urlpatterns = [
    path('', views.index, name='index'),
]


