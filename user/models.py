from django.db import models
from django.contrib.auth.models import User
from base.models import Country, State, Municipality, Parish, Clap
from django.utils.translation import ugettext_lazy as _
from base.constant import LEVEL

# Create your models here.

class Profile(models.Model):
    """!
    Clase que gestiona el perfil de los usuarios

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    """

    ## Establece el teléfono del usuario
    phone = models.CharField(
        _('teléfono'), max_length=15,
    )

    ## Establece el nivel que tiene el usuario en el sistema
    level = models.IntegerField(_('nivel'), choices=LEVEL)

    ## Establece la relación con el usuario de django
    user = models.OneToOneField(
        User, help_text=_('Relación entre los datos de registro y el usuario con acceso al sistema.'),
        on_delete=models.CASCADE, verbose_name=_('usuario')
    )

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (paez.william8 at gmail.com)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        return '%s %s' % (self.user.first_name, self.user.last_name)

    class Meta:
        """!
        Meta clase para la representación en singular y plural de la clase

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        verbose_name = _('Perfil')
        verbose_name_plural = _('Perfiles')

class NationalLevel(models.Model):

    country = models.OneToOneField(
        Country, on_delete=models.CASCADE, verbose_name=_('país')
    )

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name=_('perfil')
    )

    def __str__(self):
        return '%s %s' % (self.profile.user.first_name, self.profile.user.last_name)

    class Meta:
        verbose_name = _('Nivel Nacional')
        verbose_name_plural = _('Niveles Nacionales')

class StateLevel(models.Model):
    """!
    Clase que gestiona el perfil de los usuarios que pertenecen al nivel estadal

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    """

    ## Establec la relación con el estado
    state = models.OneToOneField(
        State, on_delete=models.CASCADE, verbose_name=_('estado')
    )

    ## Establec la relación con el perfil
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name=_('perfil')
    )

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (paez.william8 at gmail.com)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        return '%s %s' % (self.profile.user.first_name, self.profile.user.last_name)

    class Meta:
        """!
        Meta clase para la representación en singular y plural de la clase

        @author William Páez (paez.william8 at gmail.com)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        verbose_name = _('NIvel Estadal')
        verbose_name_plural = _('Niveles Estadales')

class MunicipalityLevel(models.Model):
    """!
    Clase que gestiona el perfil de los usuarios que pertenecen al nivel municipal

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    """

    ## Establec la relación con el municipio
    municipality = models.OneToOneField(
        Municipality, on_delete=models.CASCADE, verbose_name=_('municipio')
    )

    ## Establece la relación con el perfil
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name=_('perfil')
    )

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (paez.william8 at gmail.com)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        return '%s %s' % (self.profile.user.first_name, self.profile.user.last_name)

    class Meta:
        """!
        Meta clase para la representación en singular y plural de la clase

        @author William Páez (paez.william8 at gmail.com)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        verbose_name = _('Nivel Municipal')
        verbose_name_plural = _('Niveles Municipales')

class ParishLevel(models.Model):
    """!
    Clase que gestiona el perfil de los usuarios que pertenecen al nivel parroquial

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    """

    ## Establece la relación con la parroquia
    parish = models.OneToOneField(
        Parish, on_delete=models.CASCADE, verbose_name=_('parroquia')
    )

    ## Establece la relación con el perfil
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name=_('perfil')
    )

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (paez.william8 at gmail.com)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        return '%s %s' % (self.profile.user.first_name, self.profile.user.last_name)

    class Meta:
        """!
        Meta clase para la representación en singular y plural de la clase

        @author William Páez (paez.william8 at gmail.com)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        verbose_name = _('Nivel Parroquial')
        verbose_name_plural = _('Niveles Parroquiales')

class ClapLevel(models.Model):
    """!
    Clase que gestiona el perfil de los usuarios que pertenecen al nivel clap

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    """

    clap = models.OneToOneField(
        Clap, on_delete=models.CASCADE, verbose_name=_('clap')
    )

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name=_('perfil')
    )

    def __str__(self):
        return '%s %s' % (self.profile.user.first_name, self.profile.user.last_name)

    class Meta:
        verbose_name = _('Nivel Clap')
        verbose_name_plural = _('Niveles Clap')

class StreetLeader(models.Model):
    """!
    Clase que gestiona el perfil de los usuarios que pertenecen al nivel Líder de Calle

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    """

    clap_level = models.OneToOneField(
        ClapLevel, on_delete=models.CASCADE, verbose_name=_('nivel clap')
    )

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name=_('perfil')
    )

    def __str__(self):
        return '%s %s' % (self.profile.user.first_name, self.profile.user.last_name)

    class Meta:
        verbose_name = _('Lider de Calle')
        verbose_name_plural = _('Líderes de Calle')

class FamilyGroup(models.Model):

    street_leader = models.ForeignKey(
        StreetLeader,on_delete=models.CASCADE, verbose_name=_('líder de calle')
    )

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name=_('perfil')
    )

    def __str__(self):
        return '%s %s' % (self.profile.user.first_name, self.profile.user.last_name)

    class Meta:
        verbose_name = _('Grupo Familiar')
        verbose_name_plural = _('Grupos Familiares')
