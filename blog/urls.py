from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/new/', views.create, name='create'),
    path('post/<slug:slug>/', views.detail, name='detail'),
    path('post/<slug:slug>/edit/', views.edit, name='edit'),
    path('post/<slug:slug>/delete/', views.delete, name='delete'),
    path('post/<slug:slug>/like-toggle/', views.toggle_like, name='toggle_like'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
]


