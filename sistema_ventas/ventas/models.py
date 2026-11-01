from django.db import models
from django.contrib.auth.models import User

class Tienda(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, default="Mi Tienda")
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, null=True, blank=True)
    codigo = models.CharField(max_length=50, blank=True)
    nombre = models.CharField(max_length=100)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    foto = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre