from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Tienda

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nombre_tienda = request.POST.get('nombre_tienda')
        tipo_negocio = request.POST.get('tipo_negocio')
        ruc = request.POST.get('ruc')
        direccion = request.POST.get('direccion')

        if User.objects.filter(username=username).exists():
            return render(request, 'ventas/registro.html', {'error': 'El usuario ya existe'})

        user = User.objects.create_user(username=username, password=password)
        Tienda.objects.create(
            usuario=user,
            nombre_tienda=nombre_tienda,
            tipo_negocio=tipo_negocio,
            ruc=ruc if ruc else None,
            direccion=direccion
        )
        login(request, user)
        return redirect('/dashboard/')

    return render(request, 'ventas/registro.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        else:
            return render(request, 'ventas/login.html', {'error': 'Usuario o clave incorrecta'})
    return render(request, 'ventas/login.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    return render(request, 'ventas/dashboard.html')

def salir_view(request):
    logout(request)
    return redirect('/login/')

def home(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return redirect('/login/')

registro = register