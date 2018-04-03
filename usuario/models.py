from django.db import models
from django.contrib.auth.models import User
from base.models import Estado, Municipio, Parroquia, Clap
from django.utils.translation import ugettext_lazy as _
from base.constant import NIVEL

# Create your models here.

class Perfil(models.Model):
    """!
    Clase que gestiona el perfil de los usuarios

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    ## Establece el teléfono del usuario
    telefono = models.CharField(
        max_length=15,
    )

    ## Establece el nivel que tiene el usuario en el sistema
    nivel = models.IntegerField(choices=NIVEL)

    ## Establece la relación con el usuario de django
    user = models.OneToOneField(
        User, related_name="perfil",
        help_text=_("Relación entre los datos de registro y el usuario con acceso al sistema"),
        on_delete=models.CASCADE
    )

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        return "%s %s" % (self.user.first_name, self.user.last_name)

    class Meta:
        """!
        Meta clase para la representación en singular y plural de la clase

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        verbose_name = _("Perfil")
        verbose_name_plural = _("Perfiles")

class Estadal(models.Model):
    """!
    Clase que gestiona el perfil de los usuarios que pertenecen al nivel estadal

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    ## Establec la relación con el estado
    estado = models.OneToOneField(
        Estado, on_delete=models.CASCADE
    )

    ## Establec la relación con el perfil
    perfil = models.OneToOneField(
        Perfil, on_delete=models.CASCADE
    )

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        return "%s %s" % (self.perfil.user.first_name, self.perfil.user.last_name)

    class Meta:
        """!
        Meta clase para la representación en singular y plural de la clase

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        verbose_name = _("Estadal")
        verbose_name_plural = _("Estadales")

class Municipal(models.Model):
    """!
    Clase que gestiona el perfil de los usuarios que pertenecen al nivel municipal

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    ## Establec la relación con el municipio
    municipio = models.OneToOneField(
        Municipio, on_delete=models.CASCADE
    )

    ## Establece la relación con el perfil
    perfil = models.OneToOneField(
        Perfil, on_delete=models.CASCADE
    )

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        return "%s %s" % (self.perfil.user.first_name, self.perfil.user.last_name)

    class Meta:
        """!
        Meta clase para la representación en singular y plural de la clase

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        verbose_name = _("Municipal")
        verbose_name_plural = _("Municipales")

class Parroquial(models.Model):
    """!
    Clase que gestiona el perfil de los usuarios que pertenecen al nivel parroquial

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    ## Establece la relación con la parroquia
    parroquia = models.OneToOneField(
        Parroquia, on_delete=models.CASCADE
    )

    ## Establece la relación con el perfil
    perfil = models.OneToOneField(
        Perfil, on_delete=models.CASCADE
    )

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        return "%s %s" % (self.perfil.user.first_name, self.perfil.user.last_name)

    class Meta:
        """!
        Meta clase para la representación en singular y plural de la clase

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        verbose_name = _("Parroquial")
        verbose_name_plural = _("Parroquiales")

class JefeClap(models.Model):
    """!
    Clase que gestiona el perfil de los usuarios que pertenecen al nivel clap

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 10-03-2018
    @version 1.0.0
    """

    clap = models.OneToOneField(
        Clap, on_delete=models.CASCADE
    )

    perfil = models.OneToOneField(
        Perfil, on_delete=models.CASCADE
    )

    def __str__(self):
        return "%s %s" % (self.perfil.user.first_name, self.perfil.user.last_name)

    class Meta:
        verbose_name = _("Jefe Clap")
        verbose_name_plural = _("Jefes Claps")

class JefeFamiliar(models.Model):

    jefe_clap = models.ForeignKey(
        JefeClap,on_delete=models.CASCADE
    )

    def __str__(self):
        return "%s %s" % (self.jefe_clap.perfil.user.first_name, self.jefe_clap.perfil.user.last_name)

    class Meta:
        verbose_name = _("Jefe Familiar")
        verbose_name_plural = _("Jefes de Familias")
