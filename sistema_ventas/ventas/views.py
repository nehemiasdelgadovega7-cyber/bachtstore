from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Tienda, Producto
from .forms import RegistroTiendaForm
from django.contrib.auth.decorators import login_required

def registro(request):
    if request.method == 'POST':
        form = RegistroTiendaForm(request.POST)
        if form.is_valid():
            # Crear usuario
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            # Crear tienda con tipo de negocio - RUC es opcional y se pone adentro
            Tienda.objects.create(
                usuario=user,
                nombre_tienda=form.cleaned_data['nombre_tienda'],
                tipo_negocio=form.cleaned_data['tipo_negocio'],
                ruc=None
            )
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistroTiendaForm()
    return render(request, 'ventas/registro.html', {'form': form})

@login_required
def dashboard(request):
    try:
        tienda = Tienda.objects.get(usuario=request.user)
        if not tienda.esta_activa:
            return render(request, 'ventas/suspendido.html')
        productos = Producto.objects.filter(tienda=tienda)
    except:
        if request.user.is_superuser:
            return redirect('/admin/')
        productos = Producto.objects.none()
        tienda = None

    context = {
        'tienda': tienda,
        'total_productos': productos.count(),
        'productos_bajo': productos.filter(stock__lte=5)[:6],
    }
    return render(request, 'ventas/dashboard.html', context)