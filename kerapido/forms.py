from django import forms

from kerapido.models import Negocio


class RegistrarNegocio(forms.Form):
    name_bussiness = forms.CharField(label='Nombre del Negocio*', max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Nombre',
               }))
    logo_bussiness = forms.ImageField(label='Logotipo')
    portada_bussiness = forms.ImageField(label='Portada')
    slogan_bussiness = forms.CharField(label='Eslogan', max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Eslogan',
               }))


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
