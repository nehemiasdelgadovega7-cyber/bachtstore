from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from ventas.views import salir_view, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('salir/', salir_view, name='salir'),
    path('dashboard/', home, name='dashboard'),
    path('registro/', home, name='registro'),
]