from django.contrib import admin
from django.urls import path
from ventas.views import salir_view, home, register, dashboard, login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('salir/', salir_view, name='salir'),
    path('dashboard/', dashboard, name='dashboard'),
    path('registro/', register, name='registro'),
    path('login/', login_view, name='login'),
]