from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Country(models.Model):
    """!
    Clase que contiene los paises

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    """

    ## Nombre del pais
    name = models.CharField(max_length=80)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (paez.william8 at gmail.com)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        return self.name

class State(models.Model):
    """!
    Clase que contiene los estados que se encuentran en un país

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    """

    ## Nombre del Estado
    name = models.CharField(max_length=50)

    ## Pais en donde esta ubicado el Estado
    country = models.ForeignKey(Country,on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        return self.name

class Municipality(models.Model):
    """!
    Clase que contiene los municipios que se encuentran en un estado

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    """

    ## Nombre del Municipio
    name = models.CharField(max_length=50)

    ## Estado en donde se encuentra el Municipio
    state = models.ForeignKey(State,on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (paez.william8 at gmail.com)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        return self.name

class City(models.Model):
    """!
    Clase que contiene las ciudades que se encuentran en un estado

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    """

    ## Nombre de la Ciudad
    name = models.CharField(max_length=50)

    ## Estado en donde se encuentra ubicada la Ciudad
    state = models.ForeignKey(State,on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (paez.william8 at gmail.com)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        return self.name

class Parish(models.Model):
    """!
    Clase que contiene las parroquias que se encuentran un municipio

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    """

    ## Nombre de la Parroquia
    name = models.CharField(max_length=50)

    ## Municipio en el que se encuentra ubicada la Parroquia
    municipality = models.ForeignKey(Municipality,on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (paez.william at gmail.com)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        return self.name

class Clap(models.Model):
    """!
    Clase que contiene los clap que se encuentran en una parroquia

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    """

    ## Código único que identifica al clap
    code = models.CharField(
        max_length=20, primary_key=True
    )

    ## Nombre del Clap
    name = models.CharField(max_length=500)

    ## Parroquia en el que se encuetra ubicado el Clap
    parish = models.ForeignKey(Parish,on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (paez.william8 at gmail.com)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        return self.code + ' | ' + self.name

class Sex(models.Model):
    """!
    Clase que contiene el sexo de una persona

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    """

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Sexo')
        verbose_name_plural = _('Sexos')

class MaritalStatus(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Estado Civil')
        verbose_name_plural = _('Estados Civiles')

class FamilyRelationship(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Parentesco Familiar')
        verbose_name_plural = _('Parentescos Familiares')
