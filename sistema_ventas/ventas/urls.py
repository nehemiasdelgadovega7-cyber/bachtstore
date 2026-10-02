from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pos/', views.pos_touch, name='pos_touch'),
]