from django import forms
from django.contrib.auth.models import User
from .models import Tienda

class RegistroTiendaForm(forms.Form):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(label="Clave", widget=forms.PasswordInput)
    nombre_tienda = forms.CharField(label="Nombre de tu tienda")
    ruc = forms.CharField(label="RUC (Opcional)", required=False, max_length=11)