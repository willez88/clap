from django.utils.translation import ugettext_lazy as _

NIVEL_USUARIO = (
    (1,_('Estado Mayor de Alimentación Estadal')),
    (2,_('Estado Mayor de Alimentación Municipal')),
    (3,_('Estado Mayor de Alimentación Parroquial')),
    (4,_('Jefes Familiares')),
)

## Sexo
SEXO = (
    ('M',_('Masculino')),
    ('F',_('Femenino')),
)

## Tipo del Parentesco
PARENTESCO = (
    ## Parentesco de primer grado
    ('MA',_('Madre')),
    ('PA',_('Padre')),
    ('CN',_('Concubino(a)')),
    ('HI',_('Hijo(a)')),
    ('YE',_('Yerno(a)')),
    ('SU',_('Suegro(a)')),
    ## Parentesto de segundo grado
    ('AB',_('Abuelo(a)')),
    ('NI',_('Nieto(a)')),
    ('HE',_('Hermano(a)')),
    ('CU',_('Cuñado(a)')),
    ## Parentesco de tercer grado
    ('BI',_('Bisabuelo(a)')),
    ('BS',_('Bisnieto(a)')),
    ('TI',_('Tío(a)')),
    ('SO',_('Sobrino(a)')),
    ## Parentesco de cuarto grado
    ('PR',_('Primo(a)')),
    ('TA',_('Tio(a) Abuelo(a)')),
)

## Estado Civil
ESTADO_CIVIL = (
    ('SO',_('Soltero(a)')),
    ('CA',_('Casado(a)')),
    ('CF',_('Concubino(a) Formal')),
    ('CI',_('Concubino(a) Informal')),
    ('DI',_('Divirciado(a)')),
    ('VI',_('Viudo(a)')),
)
