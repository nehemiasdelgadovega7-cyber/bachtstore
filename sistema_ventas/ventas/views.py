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
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('/productos-stock/')
    return render(request, 'ventas/login.html')

@login_required
def dashboard(request):
    tienda, created = Tienda.objects.get_or_create(usuario=request.user, defaults={'nombre_tienda': 'Mi Tienda BachtStore'})
    return render(request, 'ventas/dashboard.html', {'tienda': tienda})

def productos_stock_view(request):
    from .models import Producto, Tienda
    from django.contrib.auth.decorators import login_required
    from django.shortcuts import render

    # Si no tiene tienda, muestra todos
    try:
        tienda = Tienda.objects.get(usuario=request.user)
        productos = Producto.objects.filter(tienda=tienda)
    except:
        productos = Producto.objects.all()
    
    return render(request, 'ventas/productos.html', {'productos': productos})

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
def registro_view(request):
    if request.method == 'POST':
        from django.contrib.auth.models import User
        from .models import Tienda
        from django.shortcuts import redirect
        from django.http import HttpResponse
        
        nombre_tienda = request.POST['nombre_tienda']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST.get('email','')

        if User.objects.filter(username=username).exists():
            return HttpResponse("Ese usuario ya existe, prueba otro - <a href='/registro/'>volver</a>")

        user = User.objects.create_user(username=username, password=password, email=email)
        tienda = Tienda.objects.create(usuario=user, nombre=nombre_tienda)
        
        from django.contrib.auth import login
        login(request, user)
        return redirect('/dashboard/')
    return render(request, 'ventas/registro.html')
def crear_admin_view(request):
    from django.contrib.auth.models import User
    from django.http import HttpResponse
    User.objects.filter(username='MOTOBACH-admin').delete()
    User.objects.create_superuser('MOTOBACH-admin', '', 'bach2024')
    return HttpResponse("✅ ADMIN CREADO: Usuario MOTOBACH-admin / Clave bach2024 - Ya puedes ir a /login/")

def register(request):
    from django.contrib.auth.models import User
    from .models import Tienda
    from django.shortcuts import render, redirect
    from django.http import HttpResponse
    from django.contrib.auth import login

    if request.method == 'POST':
        nombre_tienda = request.POST.get('nombre_tienda')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email','')

        if User.objects.filter(username=username).exists():
            return HttpResponse("Ese usuario ya existe <a href='/registro/'>volver</a>")
        
        user = User.objects.create_user(username=username, password=password, email=email)
        Tienda.objects.create(usuario=user, nombre=nombre_tienda)
        login(request, user)
        return redirect('/dashboard/')
    return render(request, 'ventas/registro.html')