from django.db import models
from django.contrib.auth.models import User

class Tienda(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_tienda = models.CharField(max_length=150)
    tipo_negocio = models.CharField(max_length=100, blank=True, null=True)
    ruc = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre_tienda

class Producto(models.Model):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=150)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre