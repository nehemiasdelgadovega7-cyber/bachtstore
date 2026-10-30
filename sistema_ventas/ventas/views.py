from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Tienda, Producto, Venta
from .forms import RegistroTiendaForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone

def registro(request):
    if request.method == 'POST':
        form = RegistroTiendaForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            Tienda.objects.create(
                usuario=user,
                nombre_tienda=form.cleaned_data['nombre_tienda'],
                ruc=form.cleaned_data['ruc']
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