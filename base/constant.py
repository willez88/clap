from django.utils.translation import ugettext_lazy as _

## Nombre del Sitio
APP_NAME = 'Clap'

## Asunto del mensaje de bienvenida
EMAIL_SUBJECT = 'Bienvenido a %s' % APP_NAME

## Nacionalidades (ABREVIADO)
NATIONALITY = (
    ('V', 'V'), ('E', 'E')
)

## Establece los diferentes niveles de un usuario
LEVEL = (
    (1, 'Nivel Nacional'),
    (2, 'Nivel Estadal'),
    (3, 'Nivel Municipal'),
    (4, 'Nivel Parroquial'),
    (5, 'Nivel Jefe de Clap'),
    (6, 'Nivel líder de calle'),
    (7, 'Nivel Grupo Familiar'),
)

## Mensaje de error para peticiones AJAX
MSG_NOT_AJAX = _('No se puede procesar la petición. '
    'Verifique que posea las opciones javascript habilitadas e intente nuevamente.')