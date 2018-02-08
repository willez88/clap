from django.urls import path
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from .views import MunicipalList, MunicipalCreate, EstadalUpdate, ParroquialList, ParroquialCreate, MunicipalUpdate, ParroquialUpdate

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('cambiar-clave/', login_required(views.PasswordChangeView.as_view(template_name='password_change_form.html')), name='password_change'),
    path('cambiar-clave-hecho/', login_required(views.PasswordChangeDoneView.as_view(template_name='password_change_done.html')), name='password_change_done'),

    path('estadal/actualizar/<int:pk>/', login_required(EstadalUpdate.as_view()), name='estadal_actualizar'),
    path('municipal/', login_required(MunicipalList.as_view()), name='municipal_listar'),
    path('municipal/registrar/', login_required(MunicipalCreate.as_view()), name='municipal_registrar'),

    path('municipal/actualizar/<int:pk>/', login_required(MunicipalUpdate.as_view()), name='municipal_actualizar'),
    path('parroquial/', login_required(ParroquialList.as_view()), name='parroquial_listar'),
    path('parroquial/registrar/', login_required(ParroquialCreate.as_view()), name='parroquial_registrar'),

    path('parroquial/actualizar/<int:pk>/', login_required(ParroquialUpdate.as_view()), name='parroquial_actualizar'),
]
