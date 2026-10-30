from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pos/', views.pos_touch, name='pos'),
    path('clientes/', views.dashboard, name='clientes'),
    path('reportes/', views.dashboard, name='reportes'),
    path('inventario/', views.dashboard, name='inventario'),
]