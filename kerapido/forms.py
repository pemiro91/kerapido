from django import forms
from django.forms import Select

from kerapido.models import Categoria_Producto, Producto, Negocio, Municipio, Frecuencia


class UpdateBusiness(forms.ModelForm):

    class Meta:
        model = Negocio
        fields = ['nombre', 'logo', 'portada', 'eslogan']

        labels = {
            "nombre": "Nombre del Negocio*",
            "logo": "Logotipo"
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control text', 'placeholder': 'Escriba el nombre del '
                                                                                          'negocio', }),
            'eslogan': forms.TextInput(attrs={'class': 'form-control text', 'placeholder': 'Escriba el eslogan', }),
        }


class MyForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria_Producto.objects.all())

    class Meta:
        model = Producto
        fields = ['imagen', 'nombre', 'descripcion', 'precio', 'categoria']

        labels = {
            "nombre": "Nombre*",
            "descripcion": "Descripción",
            "precio": "Precio*",
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control text', 'placeholder': 'Escriba el nombre del '
                                                                                          'producto', }),
            'descripcion': forms.TextInput(attrs={'class': 'form-control text', 'placeholder': 'Escriba la '
                                                                                               'descripción del '
                                                                                               'producto', }),
            'precio': forms.TextInput(
                attrs={'class': 'form-control text', 'placeholder': 'Escriba el precio del producto', }),

            # 'categoria': Select(attrs={'class': 'select', 'data-live-search': 'true'}),
        }
