from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import EstadalUpdateForm, MunicipalForm, ParroquialForm, MunicipalUpdateForm, ParroquialUpdateForm, JefeClapForm, JefeClapUpdateForm
from .models import Perfil, Estadal, Municipal, Parroquial, JefeClap
from django.contrib.auth.models import User
from base.models import Estado, Municipio, Parroquia, Clap

# Create your views here.

class EstadalUpdate(UpdateView):
    """!
    clase que actualiza los datos de un usuario del nivel estadal

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    model = User
    form_class = EstadalUpdateForm
    template_name = "usuario.estadal.actualizar.html"
    success_url = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        """!
        Función para verificar que solo el usuario del nivel estadal y además logueado pueda entrar

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        if self.request.user.id == self.kwargs['pk'] and self.request.user.perfil.nivel == 1:
            return super(EstadalUpdate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_initial(self):
        """!
        Función para inicializar los campos con valores por defecto

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        datos_iniciales = super(EstadalUpdate, self).get_initial()
        perfil = Perfil.objects.get(user=self.object)
        datos_iniciales['telefono'] = perfil.telefono
        estadal = Estadal.objects.get(perfil=perfil)
        datos_iniciales['estado'] = estadal.estado
        return datos_iniciales

    def form_valid(self, form):
        """!
        Función para verificar que el formulario sea válido

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Perfil.objects.filter(user=self.object):
            perfil = Perfil.objects.get(user=self.object)
            perfil.telefono = form.cleaned_data['telefono']
            perfil.save()
            if Estadal.objects.filter(perfil=perfil):
                estadal = Estadal.objects.get(perfil=perfil)
                estadal.estado = form.cleaned_data['estado']
                estadal.save()
        return super(EstadalUpdate, self).form_valid(form)

    def form_invalid(self, form):
        """!
        Función que se ejecuta en caso de que el formulario sea inválido

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        print(form.errors)
        return super(EstadalUpdate, self).form_invalid(form)

class MunicipalList(ListView):
    """!
    Clase para mostrar los usuarios del nivel municipal que pertenecen al estado quel el usuario del nivel estadal representa

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    model = Municipal
    template_name = "usuario.municipal.listar.html"

    def dispatch(self, request, *args, **kwargs):
        """!
        Función para verificar que solo el usuario del nivel estadal pueda entrar

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        if self.request.user.perfil.nivel == 1:
            return super(MunicipalList, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_queryset(self):
        """!
        Función para filtrar los usuarios del nivel municipal que pertenecen al estado quel el usuario del nivel estadal representa

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        if Estadal.objects.filter(perfil=self.request.user.perfil):
            estadal = Estadal.objects.get(perfil=self.request.user.perfil)
            queryset = Municipal.objects.filter(municipio__estado=estadal.estado)
            return queryset

class MunicipalCreate(CreateView):
    """!
    clase que registra usuarios del nivel municipal

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    model = User
    form_class = MunicipalForm
    template_name = "usuario.municipal.registrar.html"
    success_url = reverse_lazy('municipal_listar')

    def dispatch(self, request, *args, **kwargs):
        """!
        Función para verificar que solo el usuario del nivel estadal pueda entrar

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        if self.request.user.perfil.nivel == 1:
            return super(MunicipalCreate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_form_kwargs(self):
        """!
        Función que envía los datos del usuario logueado al formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        kwargs = super(MunicipalCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """!
        Función para verificar que el formulario sea válido

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.set_password(form.cleaned_data['password'])
        self.object.is_active = True
        self.object.save()

        user = User.objects.get(username=self.object.username)
        perfil = Perfil.objects.create(
            telefono=form.cleaned_data['telefono'],
            nivel = 2,
            user= user
        )

        municipio = Municipio.objects.get(pk=form.cleaned_data['municipio'])
        Municipal.objects.create(
            municipio = municipio,
            perfil = perfil
        )
        return super(MunicipalCreate, self).form_valid(form)

    def form_invalid(self, form):
        """!
        Función que se ejecuta en caso de que el formulario sea inválido

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        print(form.errors)
        return super(MunicipalCreate, self).form_invalid(form)

class MunicipalUpdate(UpdateView):
    """!
    clase que actualiza los datos de un usuario del nivel municipal

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    model = User
    form_class = MunicipalUpdateForm
    template_name = "usuario.municipal.actualizar.html"
    success_url = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        """!
        Función para verificar que solo el usuario del nivel municipal y además logueado pueda entrar

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        if self.request.user.id == self.kwargs['pk'] and self.request.user.perfil.nivel == 2:
            return super(MunicipalUpdate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_form_kwargs(self):
        """!
        Función que envía los datos del usuario logueado al formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        kwargs = super(MunicipalUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        """!
        Función para inicializar los campos con valores por defecto

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        datos_iniciales = super(MunicipalUpdate, self).get_initial()
        perfil = Perfil.objects.get(user=self.object)
        datos_iniciales['telefono'] = perfil.telefono
        municipal = Municipal.objects.get(perfil=perfil)
        datos_iniciales['municipio'] = municipal.municipio.id
        return datos_iniciales

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Perfil.objects.filter(user=self.object):
            perfil = Perfil.objects.get(user=self.object)
            perfil.telefono = form.cleaned_data['telefono']
            perfil.save()
            if Municipal.objects.filter(perfil=perfil):
                municipal = Municipal.objects.get(perfil=perfil)
                municipio = Municipio.objects.get(pk=form.cleaned_data['municipio'])
                municipal.municipio = municipio
                municipal.save()
        return super(MunicipalUpdate, self).form_valid(form)

    def form_invalid(self, form):
        """!
        Función que se ejecuta en caso de que el formulario sea inválido

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        print(form.errors)
        return super(MunicipalUpdate, self).form_invalid(form)

class ParroquialList(ListView):
    """!
    Clase para mostrar los usuarios del nivel parroquial que pertenecen al municipio quel el usuario del nivel municipal representa

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    model = Parroquial
    template_name = "usuario.parroquial.listar.html"

    def dispatch(self, request, *args, **kwargs):
        """!
        Función para verificar que solo el usuario del nivel estadal y municipal pueda entrar

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        user = User.objects.get(username=self.request.user.username)
        if user.perfil.nivel == 1 or user.perfil.nivel == 2:
            return super(ParroquialList, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_queryset(self):
        """!
        Función para filtrar los usuarios del nivel parroquial que pertenecen al municipio quel el usuario del nivel estadal representa

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        ## usuario estadal puede ver al nivel parroquial
        if Estadal.objects.filter(perfil=self.request.user.perfil):
            estadal = Estadal.objects.get(perfil=self.request.user.perfil)
            queryset = Parroquial.objects.filter(parroquia__municipio__estado=estadal.estado)
            return queryset

        ## usuario municipal puede ver al parroquial
        if Municipal.objects.filter(perfil=self.request.user.perfil):
            municipal = Municipal.objects.get(perfil=self.request.user.perfil)
            queryset = Parroquial.objects.filter(parroquia__municipio=municipal.municipio)
            return queryset

class ParroquialCreate(CreateView):
    """!
    clase que registra usuarios del nivel parroquial

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    model = User
    form_class = ParroquialForm
    template_name = "usuario.parroquial.registrar.html"
    success_url = reverse_lazy('parroquial_listar')

    def dispatch(self, request, *args, **kwargs):
        """!
        Función para verificar que solo el usuario del nivel municipal pueda entrar

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        if self.request.user.perfil.nivel == 2:
            return super(ParroquialCreate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_form_kwargs(self):
        """!
        Función que envía los datos del usuario logueado al formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        kwargs = super(ParroquialCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """!
        Función para verificar que el formulario sea válido

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.set_password(form.cleaned_data['password'])
        self.object.is_active = True
        self.object.save()

        user = User.objects.get(username=self.object.username)
        perfil = Perfil.objects.create(
            telefono=form.cleaned_data['telefono'],
            nivel = 3,
            user= user
        )

        parroquia = Parroquia.objects.get(pk=form.cleaned_data['parroquia'])
        Parroquial.objects.create(
            parroquia = parroquia,
            perfil = perfil
        )
        return super(ParroquialCreate, self).form_valid(form)

    def form_invalid(self, form):
        """!
        Función que se ejecuta en caso de que el formulario sea inválido

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        print(form.errors)
        return super(ParroquialCreate, self).form_invalid(form)

class ParroquialUpdate(UpdateView):
    """!
    clase que actualiza los datos de un usuario del nivel parroquial

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    model = User
    form_class = ParroquialUpdateForm
    template_name = "usuario.parroquial.actualizar.html"
    success_url = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        """!
        Función para verificar que solo el usuario del nivel parroquial y además logueado pueda entrar

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        if self.request.user.id == self.kwargs['pk'] and self.request.user.perfil.nivel == 3:
            return super(ParroquialUpdate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_form_kwargs(self):
        """!
        Función que envía los datos del usuario logueado al formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        kwargs = super(ParroquialUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        """!
        Función para inicializar los campos con valores por defecto

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        datos_iniciales = super(ParroquialUpdate, self).get_initial()
        perfil = Perfil.objects.get(user=self.object)
        datos_iniciales['telefono'] = perfil.telefono
        parroquial = Parroquial.objects.get(perfil=perfil)
        datos_iniciales['parroquia'] = parroquial.parroquia.id
        return datos_iniciales

    def form_valid(self, form):
        """!
        Función para verificar que el formulario sea válido

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Perfil.objects.filter(user=self.object):
            perfil = Perfil.objects.get(user=self.object)
            perfil.telefono = form.cleaned_data['telefono']
            perfil.save()
            if Parroquial.objects.filter(perfil=perfil):
                parroquial = Parroquial.objects.get(perfil=perfil)
                parroquia = Parroquia.objects.get(pk=form.cleaned_data['parroquia'])
                parroquial.parroquia = parroquia
                parroquial.save()
        return super(ParroquialUpdate, self).form_valid(form)

    def form_invalid(self, form):
        """!
        Función que se ejecuta en caso de que el formulario sea inválido

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        print(form.errors)
        return super(ParroquialUpdate, self).form_invalid(form)


class JefeClapList(ListView):
    model = JefeClap
    template_name = "usuario.jefe.clap.listar.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.perfil.nivel == 1 or self.request.user.perfil.nivel == 3:
            return super(JefeClapList, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_queryset(self):
        ## usuario estadal puede ver al nivel clap
        if Estadal.objects.filter(perfil=self.request.user.perfil):
            estadal = Estadal.objects.get(perfil=self.request.user.perfil)
            queryset = JefeClap.objects.filter(clap__parroquia__municipio__estado=estadal.estado)
            return queryset

        ## usuario parroquial puede ver al clap
        if Parroquial.objects.filter(perfil=self.request.user.perfil):
            parroquial = Parroquial.objects.get(perfil=self.request.user.perfil)
            queryset = JefeClap.objects.filter(clap__parroquia=parroquial.parroquia)
            return queryset

class JefeClapCreate(CreateView):
    model = User
    form_class = JefeClapForm
    template_name = "usuario.jefe.clap.registrar.html"
    success_url = reverse_lazy('jefe_clap_listar')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.perfil.nivel == 3:
            return super(JefeClapCreate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_form_kwargs(self):
        kwargs = super(JefeClapCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.set_password(form.cleaned_data['password'])
        self.object.is_active = True
        self.object.save()

        user = User.objects.get(username=self.object.username)
        perfil = Perfil.objects.create(
            telefono=form.cleaned_data['telefono'],
            nivel = 4,
            user= user
        )

        clap = Clap.objects.get(pk=form.cleaned_data['consejo_comunal'])
        JefeClap.objects.create(
            clap = clap,
            perfil = perfil
        )
        return super(JefeClapCreate, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(JefeClapCreate, self).form_invalid(form)

class JefeClapUpdate(UpdateView):
    model = User
    form_class = JefeClapUpdateForm
    template_name = "usuario.jefe.clap.actualizar.html"
    success_url = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.perfil.nivel == 4:
            return super(JefeClapUpdate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_form_kwargs(self):
        kwargs = super(JefeClapUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        datos_iniciales = super(JefeClapUpdate, self).get_initial()
        perfil = Perfil.objects.get(user=self.object)
        datos_iniciales['telefono'] = perfil.telefono
        jefe_clap = JefeClap.objects.get(perfil=perfil)
        datos_iniciales['clap'] = jefe_clap.clap.codigo
        return datos_iniciales

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Perfil.objects.filter(user=self.object):
            perfil = Perfil.objects.get(user=self.object)
            perfil.telefono = form.cleaned_data['telefono']
            perfil.save()
            if JefeClap.objects.filter(perfil=perfil):
                jefe_clap = JefeClap.objects.get(perfil=perfil)
                clap = Clap.objects.get(pk=form.cleaned_data['clap'])
                jefe_clap.clap = clap
                jefe_clap.save()
        return super(JefeClapUpdate, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(JefeClapUpdate, self).form_invalid(form)
