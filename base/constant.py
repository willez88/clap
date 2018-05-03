from django.utils.translation import ugettext_lazy as _

## Nombre del Sitio
APP_NAME = "Clap"

## Asunto del mensaje de bienvenida
EMAIL_SUBJECT_REGISTRO = "Bienvenido a %s" % APP_NAME

## Nacionalidades (ABREVIADO)
NACIONALIDAD = (
    ('V', 'V'), ('E', 'E')
)

## Establece los diferentes niveles de un usuario
NIVEL = (
    (0, 'administrador'),
    (1, 'Nivel Nacional'),
    (2, 'Nivel Estadal'),
    (3, 'Nivel Municipal'),
    (4, 'Nivel Parroquial'),
    (5, 'Nivel Jefe de Clap'),
    #(5, 'Nivel Jefe Familiar'),
)

## Mensaje de error para peticiones AJAX
MSG_NOT_AJAX = _("No se puede procesar la petición. "
                 "Verifique que posea las opciones javascript habilitadas e intente nuevamente.")

## Tipo de Tenencia
TIPO_TENENCIA = (
    ("PR",_("Propia Pagada")),
    ("AL",_("Alquilada")),
    ("PO",_("Propia Pagando")),
    ("HE",_("Heredada")),
    ("CE",_("Cedida")),
    ("PE",_("Prestada")),
    ("EC",_("En Cuido")),
    ("DE",_("Desocupada")),
)

## Sexo
SEXO = (
    ("M",_("Masculino")),
    ("F",_("Femenino")),
)

## Tipo del Parentesco
PARENTESCO = (
    #("JF",_("Jefe Familiar")),
    ## Parentesco de primer grado
    ("MA",_("Madre")),
    ("PA",_("Padre")),
    ("ES",_("Esposo(a)")),
    ("CN",_("Concubino(a)")),
    ("HI",_("Hijo(a)")),
    ("YE",_("Yerno(a)")),
    ("SU",_("Suegro(a)")),
    ## Parentesto de segundo grado
    ("AB",_("Abuelo(a)")),
    ("NI",_("Nieto(a)")),
    ("HE",_("Hermano(a)")),
    ("CU",_("Cuñado(a)")),
    ## Parentesco de tercer grado
    ("BI",_("Bisabuelo(a)")),
    ("BS",_("Bisnieto(a)")),
    ("TI",_("Tío(a)")),
    ("SO",_("Sobrino(a)")),
    ## Parentesco de cuarto grado
    ("PR",_("Primo(a)")),
    ("TA",_("Tio(a) Abuelo(a)")),
)

## Estado Civil
ESTADO_CIVIL = (
    ("SO",_("Soltero(a)")),
    ("CA",_("Casado(a)")),
    ("CF",_("Concubino(a) Formal")),
    ("CI",_("Concubino(a) Informal")),
    ("DI",_("Divirciado(a)")),
    ("VI",_("Viudo(a)")),
)

## Grado de Instrucción
GRADO_INSTRUCCION = (
    ("NE",_("No Estudió")),
    ("LA",_("Lactante")),
    ("PR",_("Preescolar")),
    ("1G",_("Primer Grado")),
    ("2G",_("Segundo Grado")),
    ("3G",_("Tercer Grado")),
    ("4G",_("Cuarto Grado")),
    ("5G",_("Quinto Grado")),
    ("6G",_("Sexto Grado")),
    ("7G",_("Septimo Grado")),
    ("8G",_("Octavo Grado")),
    ("9G",_("Noveno Grado")),
    ("1A",_("Primer Año Diversificado")),
    ("2A",_("Segundo Año Diversificado")),
    ("BA",_("Bachiller")),
    ("TM",_("Técnico Medio")),
    ("TS",_("Técnico Superior Universitario")),
    ("UN",_("Universitario")),
)

## Misión Educativa
MISION_EDUCATIVA = (
    ("NI",_("Ninguna")),
    ("R1",_("Misión Robinson 1")),
    ("R2",_("Misión Robinson 2")),
    ("MR",_("Misión Rivas")),
    ("MS",_("Misión Sucre")),
    ("MA",_("Misión Alma Mater")),
    ("MC",_("Misión Ciencia")),
    ("PA",_("Misión Cultura Corazón Abierto")),
    ("MM",_("Misión Música")),
)

MISION_SOCIAL = (
    ("NI",_("Ninguna")),
    ("HP",_("Hogares de la Patria")),
    ("NH",_("Negra Hipólita")),
    ("JG",_("José Gregorio Hernández")),
    ("BA",_("Barrio Adentro Deportivo")),
    ("EA",_("En Amor Mayor")),
    ("NE",_("Nevado")),
    ("JP",_("Jóvenes de la Patria")),
    ("ID",_("Identidad")),
    ("GP",_("Guaicaipuro y Piar")),
    ("MB",_("Madres del Barrio")),
)

TIPO_INGRESO = (
    ("NI",_("Ninguno")),
    ("ME",_("Menos de un Sueldo Mínimo")),
    ("1S",_("1 Sueldo Mínimo")),
    ("M1",_("Más de 1 sueldo Mínimo")),
    ("2S",_("2 Sueldos Mínimos")),
    ("M2",_("Más de 2 Sueldos Mínimos")),
)

ORGANIZACION_COMUNITARIA = (
    ("CD",_("Comité Deportivo")),
    ("CS",_("Comité de Salud")),
    ("MS",_("Mesa Técnica de Seguridad")),
    ("ME",_("Mesa Técnica de Energía")),
    ("MT",_("Mesa Técnica de Tierras")),
    ("CC",_("Consejo Comunal")),
)
