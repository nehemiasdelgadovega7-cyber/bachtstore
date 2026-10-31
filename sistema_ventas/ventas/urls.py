from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registro/', views.registro, name='registro'),
    path('salir/', views.salir_view, name='salir'),
]