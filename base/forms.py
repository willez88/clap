from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import State, Municipality, Parish, Clap

class ClapAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClapAdminForm, self).__init__(*args, **kwargs)

        # Si se ha seleccionado un estado establece el listado de municipios y elimina el atributo disable
        if 'state' in self.data and self.data['state']:
            self.fields['municipality'].widget.attrs.pop('disabled')
            self.fields['municipality'].queryset=Municipality.objects.filter(state=self.data['state'])

            # Si se ha seleccionado un municipio establece el listado de parroquias y elimina el atributo disable
            if 'municipality' in self.data and self.data['municipality']:
                self.fields['parish'].widget.attrs.pop('disabled')
                self.fields['parish'].queryset=Parish.objects.filter(municipality=self.data['municipality'])

    code = forms.CharField(
        label=_('Código:'),
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _('Indique el código del clap.'),
            }
        )
    )

    name = forms.CharField(
        label=_('Nombre:'),
        max_length=500,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _('Indique el nombre del clap.'),
            }
        )
    )

    state = forms.ModelChoiceField(
        label=_('Estado:'), queryset=State.objects.all(), empty_label=_('Seleccione...'),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip',
            'title': _('Seleccione el estado en donde se encuentra ubicada.'),
        })
    )

    ## Municipio en el que se encuentra ubicada la parroquia
    municipality = forms.ModelChoiceField(
        label=_('Municipio:'), queryset=Municipality.objects.all(), empty_label=_('Seleccione...'),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'disabled': 'true',
            'title': _('Seleccione el municipio en donde se encuentra ubicada.'),
        })
    )

    ## Parroquia en donde se encuentra ubicada la dirección suministrada
    parish = forms.ModelChoiceField(
        label=_('Parroquia:'), queryset=Parish.objects.all(), empty_label=_('Seleccione...'),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'disabled': 'true',
            'title': _('Seleccione la parroquia en donde se encuentra ubicada.'),
        })
    )

    class Meta:
        model = Clap
        fields = [
            'code','name','state','municipality','parish'
        ]
