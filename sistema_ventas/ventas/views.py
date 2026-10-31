from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Tienda, Producto

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username','').strip().lower()
        password = request.POST.get('password','').strip()
        nombre_tienda = request.POST.get('nombre_tienda','').strip()
        tipo_negocio = request.POST.get('tipo_negocio','').strip()
        ruc = request.POST.get('ruc','').strip()
        direccion = request.POST.get('direccion','').strip()
        datos = request.POST
        if User.objects.filter(username=username).exists():
            return render(request, 'ventas/registro.html', {'error': f'El usuario {username} ya existe', 'datos': datos})
        user = User.objects.create_user(username=username, password=password)
        Tienda.objects.create(usuario=user, nombre_tienda=nombre_tienda, tipo_negocio=tipo_negocio, ruc=ruc, direccion=direccion)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'ventas/registro.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username','').strip().lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        return render(request, 'ventas/login.html', {'error': 'Usuario o clave incorrecta'})
    return render(request, 'ventas/login.html')

@login_required(login_url='/login/')
def dashboard(request):
    tienda = get_object_or_404(Tienda, usuario=request.user)
    productos = Producto.objects.filter(tienda=tienda)
    context = {
        'tienda': tienda,
        'total_productos': productos.count(),
        'stock_bajo': productos.filter(stock__lte=5).count(),
    }
    return render(request, 'ventas/dashboard.html', context)

@login_required(login_url='/login/')
def productos_view(request):
    tienda = get_object_or_404(Tienda, usuario=request.user)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio_venta = request.POST.get('precio_venta') or 0
        stock = request.POST.get('stock') or 0
        Producto.objects.create(tienda=tienda, nombre=nombre, precio_venta=precio_venta, stock=stock)
        return redirect('productos')
    productos = Producto.objects.filter(tienda=tienda).order_by('-id')
    return render(request, 'ventas/productos.html', {'tienda': tienda, 'productos': productos})

def salir_view(request):
    logout(request)
    return redirect('/login/')

def home(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return redirect('/login/')

registro = register
login_tienda = login_view
salir_tienda = salir_view