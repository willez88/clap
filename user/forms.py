from django import forms
from django.contrib.auth.models import User
from base.models import Country, State, Municipality, Parish, Clap
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from base.fields import IdentityCardField
from .models import NationalLevel, StateLevel, MunicipalityLevel, ParishLevel, ClapLevel

class ProfileForm(forms.ModelForm):
    """!
    Clase que contiene los campos del formulario de perfil del usuario

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    """

    ## Username para identificar al usuario, en este caso se usa la cédula
    username = IdentityCardField(
        validators=[
            validators.RegexValidator(
                r'^[VE][\d]{8}$',
                _('Introduzca un número de cédula válido. Solo se permiten números y una longitud de 8 carácteres. Se agregan ceros (0) si la longitud es de 7 o menos caracteres.')
            ),
        ], help_text=_('V00000000 ó E00000000')
    )

    ## Nombres del usuario
    first_name = forms.CharField(
        label=_('Nombres:'), max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _('Indique los Nombres.'),
            }
        )
    )

    ## Apellidos del usuario
    last_name = forms.CharField(
        label=_('Apellidos:'), max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _('Indique los Apellidos.'),
            }
        )
    )

    ## Correo del usuario
    email = forms.EmailField(
        label=_('Correo Electrónico:'), max_length=100,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control input-sm email-mask', 'data-toggle': 'tooltip',
                'title': _('Indique el correo electrónico de contacto.')
            }
        )
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

    ## Clave de acceso del usuario
    password = forms.CharField(
        label=_('Contraseña:'), max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _('Indique una contraseña de aceso al sistema.')
            }
        )
    )

    ## Confirmación de clave de acceso del usuario
    confirm_password = forms.CharField(
        label=_('Confirmar Contraseña:'), max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _('Indique nuevamente la contraseña de aceso al sistema.')
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError(_('El correo ya esta registrado.'))
        return email

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        password = self.cleaned_data.get('password')
        if password != confirm_password:
            raise forms.ValidationError(_('La contraseña no es la misma.'))

        return confirm_password

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez (paez.william8 at gmail.com)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        model = User
        exclude = ['profile','level','date_joined']

class NationalLevelUpdateForm(ProfileForm):
    """!
    Clase que contiene el formulario para poder actualizar los datos de un usuario que tiene nivel Nacional

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    """

    def __init__(self, *args, **kwargs):
        """!
        Función que inicializa el formulario

        @author William Páez (paez.william8 at gmail.com)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        super(NationalLevelUpdateForm, self).__init__(*args, **kwargs)
        self.fields['country'].required = False
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['confirm_password'].widget.attrs['disabled'] = True

    ## Estado donde se encuentra el usuario
    country = forms.CharField(
        label=_('País:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'readonly':'true',
            'title': _('Indica el nombre del país.'),
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(_('El correo ya esta registrado.'))
        return email

    def clean_confirm_password(self):
        pass

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez (paez.william8 at gmail.com)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        model = User
        exclude = [
            'profile','level','password','confirm_password','date_joined','last_login','is_active',
            'is_superuser','is_staff', 'country'
        ]

class StateLevelForm(ProfileForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(StateLevelForm, self).__init__(*args, **kwargs)
        national_level = NationalLevel.objects.get(profile=user.profile)
        state_list = [('','Selecione...')]
        for sl in State.objects.filter(country=national_level.country):
            state_list.append( (sl.id,sl) )
        self.fields['state'].choices = state_list

    state = forms.ChoiceField(
        label=_('Estado:'),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip',
            'title': _('Seleccione el estado.'),
        })
    )

    def clean_state(self):
        state = self.cleaned_data['state']

        if StateLevel.objects.filter(state=state):
            raise forms.ValidationError(_('Ya existe un usuario asignado a este estado.'))

        return state

class StateLevelUpdateForm(ProfileForm):
    """!
    Clase que contiene el formulario para poder actualizar los datos de un usuario que tiene nivel estadal

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    """

    def __init__(self, *args, **kwargs):
        """!
        Función que inicializa el formulario

        @author William Páez (paez.william8 at gmail.com)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        super(StateLevelUpdateForm, self).__init__(*args, **kwargs)
        self.fields['state'].required = False
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['confirm_password'].widget.attrs['disabled'] = True

    ## Estado donde se encuentra el usuario
    state = forms.CharField(
        label=_('Estado:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'readonly': 'true',
            'title': _('Indica el nombre del estado.'),
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(_('El correo ya esta registrado.'))
        return email

    def clean_confirm_password(self):
        pass

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        model = User
        exclude = [
            'profile','level','password','confirm_password','date_joined','last_login','is_active',
            'is_superuser','is_staff','state'
        ]

class MunicipalityLevelForm(ProfileForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MunicipalityLevelForm, self).__init__(*args, **kwargs)
        state_level = StateLevel.objects.get(profile=user.profile)
        municipality_list = [('','Selecione...')]
        for mu in Municipality.objects.filter(state=state_level.state):
            municipality_list.append( (mu.id,mu) )
        self.fields['municipality'].choices = municipality_list

    municipality = forms.ChoiceField(
        label=_('Municipio:'),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip',
            'title': _('Seleccione el municipio.'),
        })
    )

    def clean_municipality(self):
        municipality = self.cleaned_data['municipality']
        if MunicipalityLevel.objects.filter(municipality=municipality):
            raise forms.ValidationError(_('Ya existe un usuario asignado a este municipio.'))
        return municipality

class MunicipalityLevelUpdateForm(ProfileForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MunicipalityLevelUpdateForm, self).__init__(*args, **kwargs)
        self.fields['municipality'].required = False
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['confirm_password'].widget.attrs['disabled'] = True

    municipality = forms.CharField(
        label=_('Municipio:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'readonly': 'true',
            'title': _('Indica el nombre del municipio.'),
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(_('El correo ya esta registrado.'))
        return email

    def clean_confirm_password(self):
        pass

    class Meta:
        model = User
        exclude = [
            'profile','level','password','confirm_password','date_joined','last_login','is_active',
            'is_superuser','is_staff','municipality'
        ]

class ParishLevelForm(ProfileForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ParishLevelForm, self).__init__(*args, **kwargs)
        municipality_level = MunicipalityLevel.objects.get(profile=user.profile)
        parish_list = [('','Selecione...')]
        for pa in Parish.objects.filter(municipality=municipality_level.municipality):
            parish_list.append( (pa.id,pa) )
        self.fields['parish'].choices = parish_list

    parish = forms.ChoiceField(
        label=_('Parroquia:'),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip',
            'title': _('Seleccione la parroquia.'),
        })
    )

    def clean_parish(self):
        parish = self.cleaned_data['parish']
        if ParishLevel.objects.filter(parish=parish):
            raise forms.ValidationError(_('Ya existe un usuario asignado a esta parroquia.'))
        return parish

class ParishLevelUpdateForm(ProfileForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ParishLevelUpdateForm, self).__init__(*args, **kwargs)
        self.fields['parish'].required = False
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['confirm_password'].widget.attrs['disabled'] = True

    parish = forms.CharField(
        label=_('Parroquia:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'readonly': 'true',
            'title': _('Indica el nombre de la parroquia.'),
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(_('El correo ya esta registrado.'))
        return email

    def clean_confirm_password(self):
        pass

    class Meta:
        model = User
        exclude = [
            'profile','level','password','confirm_password','date_joined','last_login','is_active',
            'is_superuser','is_staff','parish'
        ]

class ClapLevelForm(ProfileForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ClapLevelForm, self).__init__(*args, **kwargs)
        parish_level = ParishLevel.objects.get(profile=user.profile)
        clap_list = [('','Selecione...')]
        for cl in Clap.objects.filter(parish=parish_level.parish):
            clap_list.append( (cl.code,cl) )
        self.fields['clap'].choices = clap_list

    clap = forms.ChoiceField(
        label=_('Clap:'),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip',
            'title': _('Seleccione el clap.'),
        })
    )

class ClapLevelUpdateForm(ProfileForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ClapLevelUpdateForm, self).__init__(*args, **kwargs)
        self.fields['clap'].required = False
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['confirm_password'].widget.attrs['disabled'] = True

    clap = forms.CharField(
        label=_('Clap:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'readonly': 'true',
            'title': _('Indica el nombre del clap.'),
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(_('El correo ya esta registrado.'))
        return email

    def clean_confirm_password(self):
        pass

    class Meta:
        model = User
        exclude = [
            'profile','level','password','confirm_password','date_joined','last_login','is_active',
            'is_superuser','is_staff','clap'
        ]

class StreetLeaderUpdateForm(ProfileForm):
    def __init__(self, *args, **kwargs):
        super(StreetLeaderUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['confirm_password'].widget.attrs['disabled'] = True

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(_('El correo ya esta registrado.'))
        return email

    def clean_confirm_password(self):
        pass

    class Meta:
        model = User
        exclude = [
            'profile','level','password','confirm_password','date_joined','last_login','is_active',
            'is_superuser','is_staff'
        ]

class FamilyGroupUpdateForm(ProfileForm):
    def __init__(self, *args, **kwargs):
        super(FamilyGroupUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['confirm_password'].widget.attrs['disabled'] = True

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(_('El correo ya esta registrado.'))
        return email

    def clean_confirm_password(self):
        pass

    class Meta:
        model = User
        exclude = [
            'profile','level','password','confirm_password','date_joined','last_login','is_active',
            'is_superuser','is_staff'
        ]
