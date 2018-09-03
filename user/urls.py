from django.urls import path
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from .views import (
    NationalLevelUpdateView, StateLevelListView, StateLevelCreateView, MunicipalityLevelListView,
    MunicipalityLevelCreateView, StateLevelUpdateView, ParishLevelListView, ParishLevelCreateView,
    MunicipalityLevelUpdateView, ClapLevelListView, ClapLevelCreateView, ClapLevelUpdateView,
    ParishLevelUpdateView, ClapLevelUpdateView, FamilyGroupListView, FamilyGroupCreateView,
    FamilyGroupUpdateView, StreetLeaderListView, StreetLeaderCreateView, StreetLeaderUpdateView
)

app_name = 'user'

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-change/', login_required(views.PasswordChangeView.as_view(template_name='user/password_change_form.html')), name='password_change'),
    path('password-change-done/', login_required(views.PasswordChangeDoneView.as_view(template_name='user/password_change_done.html')), name='password_change_done'),

    path('national-level/update/<int:pk>/', login_required(NationalLevelUpdateView.as_view()), name='national_level_update'),
    path('state-level/', login_required(StateLevelListView.as_view()), name='state_level_list'),
    path('state-level/create/', login_required(StateLevelCreateView.as_view()), name='state_level_create'),

    path('state-level/update/<int:pk>/', login_required(StateLevelUpdateView.as_view()), name='state_level_update'),
    path('municipality-level/', login_required(MunicipalityLevelListView.as_view()), name='municipality_level_list'),
    path('municipality-level/create/', login_required(MunicipalityLevelCreateView.as_view()), name='municipality_level_create'),

    path('municipality-level/update/<int:pk>/', login_required(MunicipalityLevelUpdateView.as_view()), name='municipality_level_update'),
    path('parish-level/', login_required(ParishLevelListView.as_view()), name='parish_level_list'),
    path('parish-level/create/', login_required(ParishLevelCreateView.as_view()), name='parish_level_create'),

    path('parish/update/<int:pk>/', login_required(ParishLevelUpdateView.as_view()), name='parish_level_update'),
    path('clap-level/', login_required(ClapLevelListView.as_view()), name='clap_level_list'),
    path('clap-level/create/', login_required(ClapLevelCreateView.as_view()), name='clap_level_create'),

    path('clap-level/update/<int:pk>/', login_required(ClapLevelUpdateView.as_view()), name='clap_level_update'),
    path('street-leader/', login_required(StreetLeaderListView.as_view()), name='street_leader_list'),
    path('street-leader/create/', login_required(StreetLeaderCreateView.as_view()), name='street_leader_create'),

    path('street-leader/update/<int:pk>/', login_required(StreetLeaderUpdateView.as_view()), name='street_leader_update'),
    path('family-group/', login_required(FamilyGroupListView.as_view()), name='family_group_list'),
    path('family-group/create/', login_required(FamilyGroupCreateView.as_view()), name='family_group_create'),

    path('family-group/update/<int:pk>/', login_required(FamilyGroupUpdateView.as_view()), name='family_group_update'),
]
