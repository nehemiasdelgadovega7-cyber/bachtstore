from django import forms

class RegistroTiendaForm(forms.Form):
    nombre_tienda = forms.CharField(max_length=100, label="Nombre del negocio")
    tipo_negocio = forms.ChoiceField(choices=[
        ('bodega', 'Bodega / Abarrotes'),
        ('ferreteria', 'Ferretería'),
        ('farmacia', 'Farmacia'),
        ('ropa', 'Tienda de Ropa'),
        ('restaurante', 'Restaurante'),
        ('otro', 'Otro'),
    ])
    username = forms.CharField(max_length=50, label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Clave")