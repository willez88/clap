from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import GrupoFamiliar, Persona
from base.constant import TIPO_TENENCIA, SEXO, PARENTESCO, ESTADO_CIVIL, GRADO_INSTRUCCION, MISION_EDUCATIVA, MISION_SOCIAL, TIPO_INGRESO
from base.fields import CedulaField
from django.core import validators
from usuario.models import GrupoFamiliar

class PersonaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PersonaForm, self).__init__(*args, **kwargs)

        lista_grupo_familiar = [('','Selecione...')]
        for gf in GrupoFamiliar.objects.filter(street_leader__perfil__user=user):
            lista_grupo_familiar.append( (gf.id,gf.perfil.user.username) )
        self.fields['grupo_familiar'].choices = lista_grupo_familiar

    grupo_familiar = forms.ChoiceField(
        label=_("Grupo Familiar:"),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
                'title': _("Seleccione El Grupo Familiar al cual pertenece la Persona"),
            }
        )
    )

    nombre = forms.CharField(
        label=_("Nombres:"),
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'style':'width:250px;',
                'title': _("Indique los Nombres de la Persona"),
            }
        )
    )

    apellido = forms.CharField(
        label=_("Apellidos:"),
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'style':'width:250px;',
                'title': _("Indique los Apellidos de la Persona"),
            }
        )
    )

    tiene_cedula = forms.ChoiceField(
        label=_("¿Tiene Cédula?:"),
        choices=(('S',_('Si')),)+(('N',_('No')),),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:60px;',
                'title': _("Seleccione si tiene cédula"), 'onchange': "_tiene_cedula(this.value)",
            }
        ), required = False
    )

    cedula = CedulaField(
        required=False,
        validators=[
            validators.RegexValidator(
                r'^[VE][\d]{8}$',
                _("Introduzca un número de cédula válido. Solo se permiten números y una longitud de 8 carácteres. Se agrega un 0 si la longitud es de 7 carácteres.")
            ),
        ]
    )

    ## Teléfono del usuario
    telefono = forms.CharField(
        label=_("Teléfono:"),
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-rule-required': 'true', 'data-toggle': 'tooltip', 'style':'width:250px;',
                'title': _("Indique el número telefónico de contacto"), 'data-mask': '+00-000-0000000'
            }
        ),
        validators=[
            validators.RegexValidator(
                r'^\+\d{2}-\d{3}-\d{7}$',
                _("Número telefónico inválido. Solo se permiten números y los símbolos: + -")
            ),
        ],
        help_text=_("+58-416-0000000")
    )

    correo = forms.EmailField(
        label=_("Correo Electrónico:"),
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control input-sm email-mask', 'placeholder': _("Correo de contacto"),
                'data-toggle': 'tooltip', 'size': '30', 'data-rule-required': 'true',
                'title': _("Indique el correo electrónico de contacto con la persona.")
            }
        ), required = False,
    )

    sexo = forms.ChoiceField(
        label=_("Sexo:"),
        choices=(('',_('Seleccione...')),)+SEXO,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
                'title': _("Seleccione el Sexo de la Persona"),
            }
        )
    )

    fecha_nacimiento = forms.CharField(
        label=_("Fecha de Nacimieno:"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm datepicker','style':'width:100%;',
                'readonly':'true',
                'onchange':'calcular_edad(this.value)',
            }
        )
    )

    edad = forms.CharField(
        label=_("Edad:"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'style':'width:250px;','readonly':'true',
                'title': _("Muestra la edad de la Persona"),
            }
        ),
        required = False
    )

    parentesco = forms.ChoiceField(
        label=_("Parentesco:"),
        choices=(('',_('Seleccione...')),)+PARENTESCO,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
                'title': _("Seleccione el Parentesco"),
            }
        )
    )

    jefe_familiar = forms.BooleanField(
        label=_("Jefe Familiar"),
        help_text=_("Para actualizar los datos de un Jefe Familiar es necesario quitar esta selección y guardar. Hecho los cambios se puede seleccionar de nuevo si el Jefe Familiar se mantiene o se elige otro."),
        required = False
    )

    estado_civil = forms.ChoiceField(
        label=_("Estado Civil:"),
        choices=(('',_('Seleccione...')),)+ESTADO_CIVIL,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
                'title': _("Seleccione el Estado Civil de la Persona"),
            }
        )
    )

    observacion = forms.CharField(
        label=_("Observación:"),
        widget=forms.Textarea(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'style':'width:250px;',
                'title': _("Indique alguna observación que pueda tener la persona"),
            }
        ), required = False
    )

    def clean(self):
        cleaned_data = super(PersonaForm, self).clean()
        grupo_familiar = self.cleaned_data['grupo_familiar']
        jefe_familiar = self.cleaned_data['jefe_familiar']

        c = 0
        if jefe_familiar:
            for p in Persona.objects.filter(grupo_familiar=grupo_familiar):
                if p.jefe_familiar:
                    c= c+1
        if c >= 1:
            msg = str(_("Solo puede haber un Jefe Familiar por Grupo Familiar."))
            self.add_error('jefe_familiar', msg)

    class Meta:
        model = Persona
        exclude = [
            'grupo_familiar'
        ]
