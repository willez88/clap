from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime
from user.models import FamilyGroup
from base.models import Sex, FamilyRelationship, MaritalStatus

class Person(models.Model):

    ## Nombre de la Persona
    first_name = models.CharField(max_length=100)

    ## Apellido de la Persona
    last_name = models.CharField(max_length=100)

    ## Cédula de la Persona. Si tiene o no
    identity_card = models.CharField(
        max_length=9,
        help_text=_('Cédula de Identidad del usuario.'),
        unique=True,
        null=True
    )

    # +058-416-0708340
    phone = models.CharField(
        max_length=15,
        help_text=_('Número telefónico de contacto con el usuario.'),
    )

    ## Establece el correo de la persona
    email = models.CharField(
        max_length=100, help_text=('correo@correo.com')
    )

    ## Establece el sexo de la Persona
    sex = models.ForeignKey(Sex,on_delete=models.CASCADE)

    ## Establece la fecha de nacimiento de la Persona
    birthdate = models.DateField()

    ## Establece el parentesto que tiene el jefe familiar con el resto del Grupo Familiar
    family_relationship = models.ForeignKey(FamilyRelationship,on_delete=models.CASCADE)

    family_head = models.BooleanField()

    ## Establece el Estado Civil de la Persona
    marital_status = models.ForeignKey(MaritalStatus,on_delete=models.CASCADE)

    ## Establece alguna observación que se tenga sobre la persona
    observation = models.TextField()

    ## Establece la relación con la cuenta de usuario del jefe familiar
    family_group = models.ForeignKey(FamilyGroup,on_delete=models.CASCADE)

    ## Cacula la edad en años que tiene una persona según su fecha de nacimiento
    def age(self):
        return int((datetime.date.today() - self.birthdate).days / 365.25  )
