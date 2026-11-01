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
    nombre = models.CharField(max_length=200)
    stock = models.IntegerField(default=0)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    foto = models.ImageField(upload_to='productos/', null=True, blank=True)
    codigo = models.CharField(max_length=50, blank=True)

    @property
    def ganancia(self):
        return self.precio_venta - self.precio_compra