from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Tienda

def registro_view(request):
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
        return redirect('dashboard')

    return render(request, 'ventas/registro.html')

def dashboard(request):
    return render(request, 'ventas/dashboard.html')