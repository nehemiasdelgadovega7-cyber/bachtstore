from django.contrib import admin
from .models import Tienda, Producto, Venta

@admin.register(Tienda)
class TiendaAdmin(admin.ModelAdmin):
    list_display = ('nombre_tienda', 'usuario', 'ruc', 'esta_activa', 'fecha_pago', 'creado')
    list_filter = ('esta_activa',)
    search_fields = ('nombre_tienda', 'ruc', 'usuario__username')

admin.site.register(Producto)
admin.site.register(Venta)