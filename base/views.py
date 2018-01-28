from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class InicioView(TemplateView):
    """!
    Clase para mostrar la página de inicio

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    template_name = "base.template.html"

class Error403View(TemplateView):
    """!
    Clase para mostrar error de permiso

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    template_name = "base.error.403.html"
