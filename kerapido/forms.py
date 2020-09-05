from django import forms

from kerapido.models import Negocio


class RegisterProduct(forms.Form):
    imagen = forms.ImageField(label='Imagen')
    name_product = forms.CharField(label='Nombre del producto*', max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control text',
               'placeholder': 'Escriba el nombre del producto',
               }), required=True)
    description_product = forms.Textarea(attrs={'class': 'form-control no-resize',
                                                'placeholder': 'Escriba la descripción del producto',
                                                })
    price_product = forms.CharField(label='Precio*', max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control text',
               'placeholder': 'Escriba el precio del producto',
               }), required=True)


class MyForm(forms.ModelForm):
    class Meta:
        model = Negocio
        fields = ['nombre', 'logo', 'portada', 'eslogan', 'categorias', 'servicios']
        exclude = ['usuario_negocio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre', }),
            'eslogan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', }),
            'categorias': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', }),
        }
