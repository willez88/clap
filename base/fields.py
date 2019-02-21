from django import forms
from .constant import NATIONALITY
from .widgets import IdentityCardWidget
from django.utils.translation import ugettext_lazy as _

class IdentityCardField(forms.MultiValueField):
    """!
    Clase que agrupa los campos de una cédula correspondientes a la nacionalidad y los números

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    """

    widget = IdentityCardWidget
    default_error_messages = {
        'invalid_choices': _('Debe seleccionar una nacionalidad válida')
    }

    def __init__(self, *args, **kwargs):

        error_messages = {
            'required': _('Debe indicar un número de Cédula'),
            'invalid': _('El valor indicado no es válido'),
            'incomplete': _('El número de Cédula esta incompleto')
        }

        fields = (
            forms.ChoiceField(choices=NATIONALITY),
            forms.CharField(max_length=8)
        )

        label = _('Cédula de Identidad:')

        super(IdentityCardField, self).__init__(
            error_messages=error_messages, fields=fields, label=label, require_all_fields=True, *args, **kwargs
        )

    def compress(self, data_list):
        if data_list:
            return ''.join(data_list)
        return ''
