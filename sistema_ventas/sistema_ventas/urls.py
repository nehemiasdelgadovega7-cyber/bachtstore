from django.contrib import admin
from django.urls import path
from ventas.views import salir_view, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', home, name='login'),
    path('salir/', salir_view, name='salir'),
    path('dashboard/', home, name='dashboard'),
    path('registro/', home, name='registro'),
]