from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registro/', views.registro, name='registro'),
    path('salir/', views.salir_view, name='salir'),
]
path('factura/nueva/', views.nueva_factura),
path('boleta/nueva/', views.nueva_boleta),
path('ticket/nuevo/', views.nuevo_ticket),
path('cotizacion/nueva/', views.nueva_cotizacion),
path('documentos/', views.busqueda_documentos),
path('inventarios/', views.ver_inventarios),
path('categorias/', views.categorias_view),
path('kardex/', views.kardex_view),
path('cajas/', views.mis_cajas),
path('cajas/historial/', views.historial_caja),
path('clientes/', views.clientes_view),
path('configuracion/', views.configuracion_view),