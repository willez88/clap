from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    PersonaList,
    PersonaCreate,
    PersonaUpdate,
    PersonaDelete
)

urlpatterns = [
    path('grupo-familiar/persona/', login_required(PersonaList.as_view()), name='persona_listar'),
    path('grupo-familiar/persona/registrar/', login_required(PersonaCreate.as_view()), name='persona_registrar'),
    path('grupo-familiar/persona/actualizar/<int:pk>/', login_required(PersonaUpdate.as_view()), name='persona_actualizar'),
    path('grupo-familiar/persona/eliminar/<int:pk>/', login_required(PersonaDelete.as_view()), name='persona_eliminar'),
]
