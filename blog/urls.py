from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/new/', views.create, name='create'),
    path('post/new/article/', views.create_article, name='create_article'),
    path('post/new/status/', views.create_status, name='create_status'),
    path('post/compose/', views.compose_status, name='compose_status'),
    path('post/new/poll/', views.create_poll, name='create_poll'),
    path('post/<slug:slug>/', views.detail, name='detail'),
    path('post/<slug:slug>/edit/', views.edit, name='edit'),
    path('post/<slug:slug>/delete/', views.delete, name='delete'),
    path('post/<slug:slug>/like-toggle/', views.toggle_like, name='toggle_like'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('post/<slug:slug>/vote/<int:option_id>/', views.vote_poll, name='vote_poll'),
]


