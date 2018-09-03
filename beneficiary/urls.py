from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    PersonListView, PersonCreateView, PersonUpdateView, PersonDeleteView
)

app_name = 'beneficiary'

urlpatterns = [
    path('family-group/person/', login_required(PersonListView.as_view()), name='person_list'),
    path('family-group/person/create/', login_required(PersonCreateView.as_view()), name='person_create'),
    path('family-group/person/update/<int:pk>/', login_required(PersonUpdateView.as_view()), name='person_update'),
    path('family-group/person/delete/<int:pk>/', login_required(PersonDeleteView.as_view()), name='person_delete'),
]
