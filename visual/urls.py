# visuals/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Home'),
    path('dashboard/', views.dashboard, name='dashboard'),
      path('predict/', views.predict, name='predict'),
      path('signup/', views.signup, name='signup'),
      path('login/', views.login, name='login'),
      path('logout/', views.logout, name='logout'),
]