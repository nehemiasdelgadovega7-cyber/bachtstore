from django.db import models
from django.contrib.auth.models import User

TIPOS_NEGOCIO = [
    ('bodega', 'Bodega / Abarrotes'),
    ('ferreteria', 'Ferretería'),
    ('farmacia', 'Farmacia'),
    ('ropa', 'Tienda de Ropa'),
    ('restaurante', 'Restaurante'),
    ('barberia', 'Barbería / Salón'),
    ('otro', 'Otro negocio'),
]

class Tienda(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_tienda = models.CharField(max_length=100)
    tipo_negocio = models.CharField(max_length=20, choices=TIPOS_NEGOCIO, default='bodega')
    ruc = models.CharField(max_length=11, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True)
    esta_activa = models.BooleanField(default=True, help_text="Si no paga, lo desactivas aquí")
    fecha_pago = models.DateField(null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_tienda} - {self.usuario.username}"

class Producto(models.Model):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre

class Venta(models.Model):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)