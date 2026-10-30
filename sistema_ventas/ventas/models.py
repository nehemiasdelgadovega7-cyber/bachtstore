from django.db import models
from django.contrib.auth.models import User

# 1. EMPRESA - EL DUEÑO DEL SAAS
class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=11, blank=True)
    plan = models.CharField(max_length=20, default='gratis', choices=[('gratis','Gratis'),('pro','Pro'),('premium','Premium')])
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# 2. PERFIL - CONECTA USUARIO CON EMPRESA
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, default='admin', choices=[('admin','Admin'),('vendedor','Vendedor')])

    def __str__(self):
        return f"{self.user.username} - {self.empresa.nombre}"

# 3. AHORA TUS MODELOS ANTIGUOS, PERO CON EMPRESA
class Producto(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=100, blank=True, null=True)
    TIPO_CHOICES = [('Efectivo','Efectivo'),('Plin','Plin'),('Yape','Yape')]
    tipo_pago = models.CharField(max_length=10, choices=TIPO_CHOICES, default='Efectivo')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta {self.id} - {self.empresa.nombre}"

class VentaItem(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)