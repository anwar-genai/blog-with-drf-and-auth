from django.urls import path
from . import views

app_name = 'follows'

urlpatterns = [
    path('', views.index, name='index'),
    path('people/', views.people, name='people'),
    path('toggle/<int:user_id>/', views.toggle_follow, name='toggle'),
]


