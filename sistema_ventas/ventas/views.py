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

@login_required
def dashboard(request):
    tienda, created = Tienda.objects.get_or_create(usuario=request.user, defaults={'nombre_tienda': 'Mi Tienda BachtStore'})
    return render(request, 'ventas/dashboard.html', {'tienda': tienda})

@login_required(login_url='/login/')
def productos_view(request):
    tienda, created = Tienda.objects.get_or_create(usuario=request.user, defaults={'nombre_tienda': 'Mi Tienda BachtStore'})
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

# --- BOTONES NUEVOS PARA QUE TODO FUNCIONE ---
def nueva_factura(r): return render(r, 'ventas/en_construccion.html', {'titulo':'Nueva Factura'})
def nueva_boleta(r): return render(r, 'ventas/en_construccion.html', {'titulo':'Nueva Boleta'})
def nuevo_ticket(r): return render(r, 'ventas/en_construccion.html', {'titulo':'Nuevo Ticket'})
def nueva_cotizacion(r): return render(r, 'ventas/en_construccion.html', {'titulo':'Nueva Cotización'})
def busqueda_documentos(r): return render(r, 'ventas/en_construccion.html', {'titulo':'Búsqueda de Documentos'})
def nuevo_producto(r): return redirect('/productos/')
def ver_inventarios(r): return render(r, 'ventas/en_construccion.html', {'titulo':'Ver Inventarios'})
def categorias_view(r): return render(r, 'ventas/en_construccion.html', {'titulo':'Categorías'})
def kardex_view(r): return render(r, 'ventas/en_construccion.html', {'titulo':'Kardex'})
def mis_cajas(r): return render(r, 'ventas/en_construccion.html', {'titulo':'Mis Cajas'})
def historial_caja(r): return render(r, 'ventas/en_construccion.html', {'titulo':'Historial de Caja'})
def clientes_view(r): return render(r, 'ventas/en_construccion.html', {'titulo':'Clientes'})

@login_required
def configuracion_view(request):
    # Simula guardar, si tienes modelo Tienda úsalo
    tienda = getattr(request.user, 'tienda', None)
    if request.method == 'POST':
        # Aquí guardas en tu modelo
        # tienda.ruc = request.POST.get('ruc') etc
        # tienda.save()
        print("DATOS RECIBIDOS:", request.POST)
        return redirect('configuracion')
    return render(request, 'ventas/configuracion.html', {'tienda': tienda})
registro = register
login_tienda = login_view
salir_tienda = salir_view