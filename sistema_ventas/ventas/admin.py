from django.contrib import admin
from .models import Tienda, Producto

# Intenta registrar Venta si existe, si no, no pasa nada
try:
    from .models import Venta
    admin.site.register(Venta)
except ImportError:
    pass

try:
    from .models import DetalleVenta
    admin.site.register(DetalleVenta)
except ImportError:
    pass

admin.site.register(Tienda)
admin.site.register(Producto)