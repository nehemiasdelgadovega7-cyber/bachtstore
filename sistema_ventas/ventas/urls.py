from django.urls import path
from . import views

urlpatterns = [
    path('', views.pos, name='pos'),
    path('pos/', views.pos, name='pos'),
    path('registro/', views.registro, name='registro'),
    path('super/', views.super_panel, name='super_panel'),
]