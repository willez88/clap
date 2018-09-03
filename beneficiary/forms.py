from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Person
from base.fields import IdentityCardField
from django.core import validators
from user.models import FamilyGroup
from base.models import Sex, MaritalStatus, FamilyRelationship

class PersonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PersonForm, self).__init__(*args, **kwargs)

        family_group_list = [('','Selecione...')]
        for fg in FamilyGroup.objects.filter(street_leader__profile__user=user):
            family_group_list.append( (fg.id,fg.profile.user.username) )
        self.fields['family_group'].choices = family_group_list

    family_group = forms.ChoiceField(
        label=_('Grupo Familiar:'),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': _('Seleccione El Grupo Familiar al cual pertenece la Persona.'),
            }
        )
    )

    first_name = forms.CharField(
        label=_('Nombres:'),
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _('Indique los Nombres de la Persona.'),
            }
        )
    )

    last_name = forms.CharField(
        label=_('Apellidos:'),
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _('Indique los Apellidos de la Persona.'),
            }
        )
    )

    has_identity_card = forms.ChoiceField(
        label=_('¿Tiene Cédula?:'),
        choices=(('S',_('Si')),)+(('N',_('No')),),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': _('Seleccione si tiene cédula.'), 'onchange': "_has_identity_card(this.value)",
            }
        ), required = False
    )

    identity_card = IdentityCardField(
        required=False,
        validators=[
            validators.RegexValidator(
                r'^[VE][\d]{8}$',
                _('Introduzca un número de cédula válido. Solo se permiten números y una longitud de 8 carácteres. Se agrega un 0 si la longitud es de 7 carácteres.')
            ),
        ]
    )

    ## Teléfono del usuario
    phone = forms.CharField(
        label=_('Teléfono:'),
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _('Indique el número telefónico de contacto.'), 'data-mask': '+00-000-0000000'
            }
        ),
        validators=[
            validators.RegexValidator(
                r'^\+\d{2}-\d{3}-\d{7}$',
                _('Número telefónico inválido. Solo se permiten números y los símbolos: + -')
            ),
        ],
        help_text=_('+58-416-0000000')
    )

    email = forms.EmailField(
        label=_('Correo Electrónico:'),
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control input-sm email-mask', 'placeholder': _('Correo de contacto'),
                'data-toggle': 'tooltip', 'size': '30',
                'title': _('Indique el correo electrónico de contacto con la persona.')
            }
        ), required = False,
    )

    sex = forms.ModelChoiceField(
        label=_('Sexo:'), queryset=Sex.objects.all(), empty_label=_('Seleccione...'),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': _('Seleccione el Sexo de la Persona.'),
            }
        )
    )

    birthdate = forms.CharField(
        label=_('Fecha de Nacimieno:'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm datepicker','readonly':'true',
                'onchange':'calculate_age(this.value)',
            }
        )
    )

    age = forms.CharField(
        label=_('Edad:'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip','readonly':'true',
                'title': _('Muestra la edad de la Persona.'),
            }
        ),
        required = False
    )

    family_relationship = forms.ModelChoiceField(
        label=_('Parentesco:'), queryset=FamilyRelationship.objects.all(), empty_label=_('Seleccione...'),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': _('Seleccione el Parentesco.'),
            }
        )
    )

    family_head = forms.BooleanField(
        label=_('Jefe Familiar:'),
        help_text=_('Para actualizar los datos de un Jefe Familiar es necesario quitar esta selección y guardar. Hecho los cambios se puede seleccionar de nuevo si el Jefe Familiar se mantiene o se elige otro.'),
        required = False
    )

    marital_status = forms.ModelChoiceField(
        label=_('Estado Civil:'), queryset=MaritalStatus.objects.all(), empty_label=_('Seleccione...'),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': _('Seleccione el Estado Civil de la Persona.'),
            }
        )
    )

    observation = forms.CharField(
        label=_('Observación:'),
        widget=forms.Textarea(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _('Indique alguna observación que pueda tener la persona.'),
            }
        ), required = False
    )

    def clean(self):
        cleaned_data = super(PersonForm, self).clean()
        family_group = self.cleaned_data['family_group']
        family_head = self.cleaned_data['family_head']

        c = 0
        if family_head:
            for p in Person.objects.filter(family_group=family_group):
                if p.family_head:
                    c= c+1
        if c >= 1:
            msg = str(_('Solo puede haber un Jefe Familiar por Grupo Familiar.'))
            self.add_error('family_head', msg)

    class Meta:
        model = Person
        exclude = [
            'family_group'
        ]
