from django import forms
from django.forms import Select

from kerapido.models import Categoria_Producto, Producto


# class UpdateProduct(forms.Form):
#     imagen = forms.ImageField(label='Imagen')
#     name_product = forms.CharField(label='Nombre del producto*', max_length=15, widget=forms.TextInput(
#         attrs={'class': 'form-control text',
#                'placeholder': 'Escriba el nombre del producto',
#                }), required=True)
#     description_product = forms.CharField(label='Descripción del producto', max_length=15, widget=forms.TextInput(
#         attrs={'class': 'form-control text',
#                'placeholder': 'Escriba la descripción del producto',
#                }))
#     price_product = forms.CharField(label='Precio*', max_length=15, widget=forms.TextInput(
#         attrs={'class': 'form-control text',
#                'placeholder': 'Escriba el precio del producto',
#                }), required=True)
#     categoria = forms.IntegerField(
#         widget=forms.Select(
#             choices=Categoria_Producto.objects.all().values_list('id', 'nombre'),
#             attrs={'class': 'form-control show-tick',
#                    'data-live-search': 'true'
#                    }
#         )
#     )


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
