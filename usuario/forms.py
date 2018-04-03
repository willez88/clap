from django import forms
from django.contrib.auth.models import User
from base.models import Estado, Municipio, Parroquia, Clap
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from base.fields import CedulaField
from .models import Estadal, Municipal, Parroquial, JefeClap

class PerfilForm(forms.ModelForm):
    """!
    Clase que contiene los campos del formulario de perfil del usuario

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    ## Username para identificar al usuario, en este caso se usa la cédula
    username = CedulaField(
        validators=[
            validators.RegexValidator(
                r'^[VE][\d]{8}$',
                _("Introduzca un número de cédula válido. Solo se permiten números y una longitud de 8 carácteres. Se agregan ceros (0) si la longitud es de 7 o menos caracteres.")
            ),
        ], help_text=_("V00000000 ó E00000000")
    )

    ## Nombres del usuario
    first_name = forms.CharField(
        label=_("Nombres:"), max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'style':'width:250px;',
                'title': _("Indique los Nombres"),
            }
        )
    )

    ## Apellidos del usuario
    last_name = forms.CharField(
        label=_("Apellidos:"), max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'style':'width:250px;',
                'title': _("Indique los Apellidos"),
            }
        )
    )

    ## Correo del usuario
    email = forms.EmailField(
        label=_("Correo Electrónico:"), max_length=100,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control input-sm email-mask', 'data-toggle': 'tooltip', 'data-rule-required': 'true', 'style':'width:250px;',
                'title': _("Indique el correo electrónico de contacto")
            }
        )
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

    ## Clave de acceso del usuario
    password = forms.CharField(
        label=_("Contraseña:"), max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'data-rule-required': 'true', 'data-toggle': 'tooltip', 'style':'width:250px;',
                'title': _("Indique una contraseña de aceso al sistema")
            }
        )
    )

    ## Confirmación de clave de acceso del usuario
    verificar_contrasenha = forms.CharField(
        label=_("Verificar Contraseña:"), max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'data-rule-required': 'true', 'data-toggle': 'tooltip', 'style':'width:250px;',
                'title': _("Indique nuevamente la contraseña de aceso al sistema")
            }
        )
    )

    def clean_verificar_contrasenha(self):
        verificar_contrasenha = self.cleaned_data['verificar_contrasenha']
        contrasenha = self.data['password']
        if contrasenha != verificar_contrasenha:
            raise forms.ValidationError(_("La contraseña no es la misma"))

        return verificar_contrasenha

    class Meta:
        """!
        Meta clase del formulario que establece el modelo que se usa y los campos que se excluyen

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        model = User
        exclude = ['perfil','nivel','date_joined']

class EstadalUpdateForm(PerfilForm):
    """!
    Clase que contiene el formulario para poder actualizar los datos de un usuario que tiene nivel estadal

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        """!
        Función que inicializa el formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        super(EstadalUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['verificar_contrasenha'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['verificar_contrasenha'].widget.attrs['disabled'] = True

    ## Estado donde se encuentra el usuario
    estado = forms.ModelChoiceField(
        label=_("Estado"), queryset=Estado.objects.all(), empty_label=_("Seleccione..."),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
            'title': _("Seleccione el estado"),
        })
    )

    def clean_verificar_contrasenha(self):
        pass

    class Meta:
        """!
        Meta clase del formulario que establec el modelo que se usa y los campos que se excluyen

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        model = User
        exclude = [
            'perfil','nivel','password','verificar_contrasenha','date_joined','last_login','is_active',
            'is_superuser','is_staff'
        ]

class MunicipalForm(PerfilForm):
    """!
    Clase que contiene el formulario para que el usuario del nivel estadal registre a los usuarios del nivel municipal

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        """!
        Función que inicializa el campo municipio cargando todos los municipios que pertenecen al estado que representa el usuario del nivel estadal

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        user = kwargs.pop('user')
        super(MunicipalForm, self).__init__(*args, **kwargs)
        estadal = Estadal.objects.get(perfil=user.perfil)
        lista_municipio = [('','Selecione...')]
        for mu in Municipio.objects.filter(estado=estadal.estado):
            lista_municipio.append( (mu.id,mu.nombre) )
        self.fields['municipio'].choices = lista_municipio

    ## Establce el campo municipio
    municipio = forms.ChoiceField(
        label=_("Municipio"),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
            'title': _("Seleccione el municipio"),
        })
    )

    def clean_municipio(self):
        municipio = self.cleaned_data['municipio']

        if Municipal.objects.filter(municipio=municipio):
            raise forms.ValidationError(_("Ya existe un usuario asignado a este municipio"))

        return municipio

class MunicipalUpdateForm(PerfilForm):
    """!
    Clase que contiene el formulario para poder actualizar los datos de un usuario que tiene nivel municipal

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        """!
        Función que inicializa el formulario para omitir los campos de contraseña y cargar los municipios que pertenecen al estado que representa el usuario de nivel estadal

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        user = kwargs.pop('user')
        super(MunicipalUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['verificar_contrasenha'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['verificar_contrasenha'].widget.attrs['disabled'] = True
        municipal = Municipal.objects.get(perfil=user.perfil)
        lista_municipio = [('','Selecione...')]
        for mu in Municipio.objects.filter(estado=municipal.municipio.estado):
            lista_municipio.append( (mu.id,mu.nombre) )
        self.fields['municipio'].choices = lista_municipio

    ## Establece el campo municipio
    municipio = forms.ChoiceField(
        label=_("Municipio"),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
            'title': _("Seleccione el municipio"),
        })
    )

    def clean_verificar_contrasenha(self):
        pass

    class Meta:
        model = User
        exclude = [
            'perfil','nivel','password','verificar_contrasenha','date_joined','last_login','is_active',
            'is_superuser','is_staff'
        ]

class ParroquialForm(PerfilForm):
    """!
    Clase que contiene el formulario para que el usuario del nivel municipal registre a los usuarios del nivel parroquial

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        """!
        Función que inicializa el campo parroquia cargando todas las parroquias que pertenecen al municipio que el usuario del nivel estadal representa

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """
        user = kwargs.pop('user')
        super(ParroquialForm, self).__init__(*args, **kwargs)
        municipal = Municipal.objects.get(perfil=user.perfil)
        lista_parroquia = [('','Selecione...')]
        for pa in Parroquia.objects.filter(municipio=municipal.municipio):
            lista_parroquia.append( (pa.id,pa.nombre) )
        self.fields['parroquia'].choices = lista_parroquia

    ## Establece el campo parroquia
    parroquia = forms.ChoiceField(
        label=_("Parroquia"),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
            'title': _("Seleccione la parroquia"),
        })
    )

    def clean_parroquia(self):
        parroquia = self.cleaned_data['parroquia']

        if Parroquial.objects.filter(parroquia=parroquia):
            raise forms.ValidationError(_("Ya existe un usuario asignado a esta parroquia"))

        return parroquia

class ParroquialUpdateForm(PerfilForm):
    """!
    Clase que contiene el formulario para actualizar los datos de un usuario que tiene nivel parroquial

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        """!
        Función que inicializa el formulario para omitir los campos de contraseña y cargar las parroquias que pertenecen al municipio que el usuario de nivel municipal representa

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        user = kwargs.pop('user')
        super(ParroquialUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['verificar_contrasenha'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['verificar_contrasenha'].widget.attrs['disabled'] = True
        parroquial = Parroquial.objects.get(perfil=user.perfil)
        lista_parroquia = [('','Selecione...')]
        for pa in Parroquia.objects.filter(municipio=parroquial.parroquia.municipio):
            lista_parroquia.append( (pa.id,pa.nombre) )
        self.fields['parroquia'].choices = lista_parroquia

    ## Establece el campo parroquia
    parroquia = forms.ChoiceField(
        label=_("Parroquia"),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
            'title': _("Seleccione la parroquia"),
        })
    )

    def clean_verificar_contrasenha(self):
        pass

    class Meta:
        model = User
        exclude = [
            'perfil','nivel','password','verificar_contrasenha','date_joined','last_login','is_active',
            'is_superuser','is_staff'
        ]

class JefeClapForm(PerfilForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(JefeClapForm, self).__init__(*args, **kwargs)
        parroquial = Parroquial.objects.get(perfil=user.perfil)
        lista_clap = [('','Selecione...')]
        for cl in Clap.objects.filter(parroquia=parroquial.parroquia):
            lista_clap.append( (cl.codigo,cl.codigo + ' ' + cl.nombre) )
        self.fields['clap'].choices = lista_clap

    clap = forms.ChoiceField(
        label=_("Clap"),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
            'title': _("Seleccione el clap"),
        })
    )

    def clean_clap(self):
        clap = self.cleaned_data['clap']

        if JefeClap.objects.filter(clap=clap):
            raise forms.ValidationError(_("Ya existe un usuario asignado a este clap"))

        return clap

class JefeClapUpdateForm(PerfilForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(JefeClapUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['verificar_contrasenha'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['verificar_contrasenha'].widget.attrs['disabled'] = True
        jefe_clap= JefeClap.objects.get(perfil=user.perfil)
        lista_clap = [('','Selecione...')]
        for cl in Clap.objects.filter(parroquia=jefe_clap.clap.parroquia):
            lista_clap.append( (cl.codigo,cl.codigo + ' ' + cl.nombre) )
        self.fields['clap'].choices = lista_clap

    clap = forms.ChoiceField(
        label=_("Consejo Comunal"),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
            'title': _("Seleccione el clap"),
        })
    )

    def clean_verificar_contrasenha(self):
        pass

    class Meta:
        model = User
        exclude = [
            'perfil','nivel','password','verificar_contrasenha','date_joined','last_login','is_active',
            'is_superuser','is_staff'
        ]
