# visuals/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Home'),
    path('dashboard/', views.dashboard, name='dashboard'),
]