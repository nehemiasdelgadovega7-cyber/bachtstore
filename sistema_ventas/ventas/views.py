from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Empresa, Producto

def registro(request):
    if request.method == 'POST':
        nombre_bodega = request.POST['nombre_bodega']
        ruc = request.POST.get('ruc', '')
        username = request.POST['username']
        password = request.POST['password']

        # 1. Crea usuario
        user = User.objects.create_user(username=username, password=password)
        
        # 2. Crea su empresa automáticamente (aislada)
        tipo = 'FORMAL' if ruc else 'INFORMAL'
        empresa = Empresa.objects.create(
            nombre=nombre_bodega,
            ruc=ruc or None,
            tipo=tipo,
            dueno=user
        )
        login(request, user)
        return redirect('pos')

    return render(request, 'registro.html')

@login_required(login_url='/admin/login/')
def pos(request):
    mi_empresa = Empresa.objects.get(dueno=request.user)

    # BLOQUEO POR NO PAGO - Si no pagó, no entra
    if hasattr(mi_empresa, 'esta_activa') and not mi_empresa.esta_activa:
        return render(request, 'suspendido.html')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        if nombre and precio:
            Producto.objects.create(
                empresa=mi_empresa,
                nombre=nombre,
                precio=precio
            )
        return redirect('pos')

    productos = Producto.objects.filter(empresa=mi_empresa)
    return render(request, 'pos.html', {'productos': productos, 'empresa': mi_empresa})

@staff_member_required
def super_panel(request):
    empresas = Empresa.objects.all().order_by('-id')
    if request.method == 'POST':
        emp = Empresa.objects.get(id=request.POST.get('empresa_id'))
        # Cambia de activa a suspendida y viceversa
        emp.esta_activa = not emp.esta_activa
        emp.save()
        return redirect('super_panel')
    return render(request, 'super_panel.html', {'empresas': empresas})