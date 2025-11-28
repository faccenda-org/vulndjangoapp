"""URL patterns for vulnapp"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_user, name='search'),
    path('comments/', views.add_comment, name='comments'),
    path('login/', views.login, name='login'),
    path('profile/', views.user_profile, name='profile'),
]
