from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.register, name='registro'),
    path('logout/', views.salir_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('productos/', views.productos_view, name='productos'),
    path('facturacion/', views.nueva_factura, name='facturacion'),
    path('productos-stock/', views.productos_view, name='productos_stock'),
    path('punto-venta/', views.nuevo_ticket, name='punto_venta'),
    path('configuracion/', views.configuracion_view, name='configuracion'),
    path('clientes/', views.clientes_view, name='clientes'),
    path('cajas/', views.mis_cajas, name='cajas'),
    path('nueva-factura/', views.nueva_factura, name='nueva_factura'),
    path('nueva-boleta/', views.nueva_boleta, name='nueva_boleta'),
    path('nuevo-ticket/', views.nuevo_ticket, name='nuevo_ticket'),
]