from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Producto, Venta
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

@login_required
def dashboard(request):
    productos = Producto.objects.filter(user=request.user)
    ventas_hoy = Venta.objects.filter(user=request.user, fecha__date=timezone.now().date())
    ingreso_hoy = ventas_hoy.aggregate(Sum('total'))['total__sum'] or 0
    stock_bajo = productos.filter(stock__lte=5).count()
    
    # Para el gráfico de 7 días
    ultimos_7_dias = []
    for i in range(7):
        dia = timezone.now().date() - timedelta(days=i)
        total = Venta.objects.filter(user=request.user, fecha__date=dia).aggregate(Sum('total'))['total__sum'] or 0
        ultimos_7_dias.append({'dia': dia.strftime('%a'), 'total': float(total)})
    ultimos_7_dias.reverse()

    context = {
        'ingreso': ingreso_hoy,
        'total_productos': productos.count(),
        'stock_bajo_count': stock_bajo,
        'productos_bajo': productos.filter(stock__lte=5)[:6],
        'mas_vendidos': productos.order_by('-stock')[:4], # temporal
        'ventas_7_dias': ultimos_7_dias,
        'transacciones_hoy': ventas_hoy.count()
    }
    return render(request, 'sistema_ventas/dashboard.html', context)

@login_required
def pos_touch(request):
    productos = Producto.objects.filter(user=request.user)
    categoria = request.GET.get('cat')
    if categoria and categoria != 'Todos':
        productos = productos.filter(categoria=categoria)
    return render(request, 'pos_touch.html', {'productos': productos})