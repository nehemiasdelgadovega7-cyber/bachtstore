from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, default='Lácteos', choices=[('Lácteos','Lácteos'),('Granos','Granos'),('Bebidas','Bebidas'),('Panadería','Panadería'),('Frutas','Frutas')])
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    codigo_barras = models.CharField(max_length=50, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, blank=True)
    deuda = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Venta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=[('Yape','Yape'),('Plin','Plin'),('Efectivo','Efectivo'),('Tarjeta','Tarjeta')])
    fecha = models.DateTimeField(auto_now_add=True)