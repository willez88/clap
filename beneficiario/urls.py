from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    GrupoFamiliarList,
    GrupoFamiliarCreate,
    GrupoFamiliarUpdate,
    GrupoFamiliarDelete,
    PersonaList,
    PersonaCreate,
    PersonaUpdate,
    PersonaDelete
)

urlpatterns = [

    #url(r'^grupo-familiar/$', login_required(GrupoFamiliarList.as_view()), name='grupo_familiar_listar'),
    #url(r'^grupo-familiar/registrar/$', login_required(GrupoFamiliarCreate.as_view()), name='grupo_familiar_registrar'),
    #url(r'^grupo-familiar/actualizar/(?P<pk>\d+)/$', login_required(GrupoFamiliarUpdate.as_view()), name='grupo_familiar_actualizar'),
    #url(r'^grupo-familiar/eliminar/(?P<pk>\d+)/$', login_required(GrupoFamiliarDelete.as_view()), name='grupo_familiar_eliminar'),
    #url(r'^persona/', include('vivienda.grupo_familiar.persona.urls')),
    path('grupo-familiar/persona/', login_required(PersonaList.as_view()), name='persona_listar'),
    path('grupo-familiar/persona/registrar/', login_required(PersonaCreate.as_view()), name='persona_registrar'),
    path('grupo-familiar/persona/actualizar/<int:pk>/', login_required(PersonaUpdate.as_view()), name='persona_actualizar'),
    path('grupo-familiar/persona/eliminar/<int:pk>/', login_required(PersonaDelete.as_view()), name='persona_eliminar'),
]
