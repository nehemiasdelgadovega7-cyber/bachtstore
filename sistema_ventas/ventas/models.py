from django.db import models
from django.contrib.auth.models import User

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=11, null=True, blank=True)
    tipo = models.CharField(max_length=20)
    dueno = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    esta_activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)