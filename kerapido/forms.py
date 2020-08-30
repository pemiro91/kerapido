from django import forms
from .models import Provincia, Municipio, Negocio


class ProvinciaForm(forms.ModelForm):
    class Meta:
        model = Negocio
        fields = ('nombre', 'birthdate', 'country', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['provincia'].queryset = Municipio.objects.none()
