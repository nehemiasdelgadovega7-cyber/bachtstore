from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import logout
from django.shortcuts import redirect

def salir_fix(request):
    logout(request)
    request.session.flush()
    return redirect('/')

def login_fix(request):
    return redirect('/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('salir/', salir_fix, name='salir'),
    path('login/', login_fix, name='login'),
    path('', include('ventas.urls')),
]