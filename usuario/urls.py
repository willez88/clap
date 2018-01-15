from django.urls import path
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('cambiar-clave/', login_required(views.PasswordChangeView.as_view(template_name='password_change_form.html')), name='password_change'),
    path('cambiar-clave-hecho/', login_required(views.PasswordChangeDoneView.as_view(template_name='password_change_done.html')), name='password_change_done'),
]
