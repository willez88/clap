from django.db import models
from django.contrib.auth.models import User
from base.models import Clap
from django.utils.translation import ugettext_lazy as _
from base.constant import SEXO, ESTADO_CIVIL, PARENTESCO, NIVEL_USUARIO

# Create your models here.

class Perfil(models.Model):

    ## Cédula de la Persona. Si tiene o no
    cedula = models.CharField(max_length=9, help_text=_('Cédula de Identidad del usuario'), unique=True, null=True)

    ## +058-416-0708340
    telefono = models.CharField(max_length=16, help_text=_('Número telefónico de contacto con el usuario'))

    ## Establece el sexo de la Persona
    sexo = models.CharField(max_length=1, choices=SEXO)

    ## Establece la fecha de nacimiento del usuario
    fecha_nacimiento = models.DateField()

    ## Establece el Estado Civil de la Persona
    estado_civil = models.CharField(max_length=2, choices=ESTADO_CIVIL)

    ## Establece el parentesto que tiene el jefe familiar con el resto del Grupo Familiar
    parentesco = models.CharField(max_length=2, choices=PARENTESCO)

    ## Establece quien es el Jefe Familiar (usuario que puede entrar al sistema para consultar)
    jefe_familiar = models.BooleanField(default=False)

    ## Clap al que pertenece el usuario (ubicación geográfica)
    clap = models.ForeignKey(Clap, on_delete=models.CASCADE)

    ## Establece la dirección donde vive el usuario
    direccion = models.CharField(max_length=500)

    ## Nivel de usuario (Este será el último nivel, usuario limitado)
    nivel_usuario = models.IntegerField()

    ## Establece la relación con el usuario registrado
    user = models.OneToOneField(User, help_text=_('Relación entre los datos del Jefe Familiar y los datos del usuario del sistema'),
        on_delete=models.CASCADE
    )

    ## Establece la relación consigo mismo para que los parientes queden relacionados con el Jefe Familiar
    users = models.ForeignKey(User, related_name='users', help_text=_('Registra nuevos usuarios y los mantiene relacionados consigo mismo'),
        on_delete=models.CASCADE
    )

    ## Cacula la edad en años que tiene una persona según su fecha de nacimiento
    def edad(self):
        return int((datetime.date.today() - self.fecha_nacimiento).days / 365.25  )
