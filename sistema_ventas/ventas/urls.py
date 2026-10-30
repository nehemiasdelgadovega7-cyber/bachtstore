from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard2'),
    path('pos/', views.pos_touch, name='pos'),
    path('clientes/', views.dashboard, name='clientes'), # temporal hasta crear vista
    path('reportes/', views.dashboard, name='reportes'),
    path('inventario/', views.dashboard, name='inventario'),
]