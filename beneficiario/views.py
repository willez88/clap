from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import GrupoFamiliar, Persona
from usuario.models import StreetLeader
from .forms import PersonaForm
from django.contrib.auth.models import User
from usuario.models import JefeClap

class PersonaList(ListView):
    model = Persona
    template_name = "persona.listar.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.perfil.nivel == 6 or self.request.user.perfil.nivel == 7:
            return super(PersonaList, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_queryset(self):

        if StreetLeader.objects.filter(perfil=self.request.user.perfil):
            street_leader = StreetLeader.objects.get(perfil=self.request.user.perfil)
            queryset = Persona.objects.filter(grupo_familiar__street_leader__jefe_clap__clap=street_leader.jefe_clap.clap)
            print(queryset)
            return queryset

        if GrupoFamiliar.objects.filter(perfil=self.request.user.perfil):
            grupo_familiar = GrupoFamiliar.objects.get(perfil=self.request.user.perfil)
            queryset = Persona.objects.filter(grupo_familiar=grupo_familiar)
            return queryset

class PersonaCreate(CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = "persona.registrar.html"
    success_url = reverse_lazy('persona_listar')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.perfil.nivel == 6:
            return super(PersonaCreate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_form_kwargs(self):
        kwargs = super(PersonaCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        grupo_familiar = GrupoFamiliar.objects.get(pk=form.cleaned_data['grupo_familiar'])
        self.object = form.save(commit=False)
        self.object.grupo_familiar = grupo_familiar
        self.object.nombre = form.cleaned_data['nombre']
        self.object.apellido = form.cleaned_data['apellido']
        if form.cleaned_data['tiene_cedula']=="S":
            self.object.cedula = form.cleaned_data['cedula']
        else:
            self.object.cedula = None
        self.object.telefono = form.cleaned_data['telefono']
        self.object.correo = form.cleaned_data['correo']
        self.object.sexo = form.cleaned_data['sexo']
        self.object.fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
        self.object.parentesco = form.cleaned_data['parentesco']
        if form.cleaned_data['jefe_familiar']:
            self.object.jefe_familiar = form.cleaned_data['jefe_familiar']
        self.object.estado_civil = form.cleaned_data['estado_civil']
        self.object.observacion = form.cleaned_data['observacion']
        self.object.save()
        return super(PersonaCreate, self).form_valid(form)

    def form_invalid(self, form):
        return super(PersonaCreate, self).form_invalid(form)

class PersonaUpdate(UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = "persona.registrar.html"
    success_url = reverse_lazy('persona_listar')

    def get_form_kwargs(self):
        kwargs = super(PersonaUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        if not Persona.objects.filter(pk=self.kwargs['pk'],grupo_familiar__street_leader__perfil__user=user):
            return redirect('base_403')
        return super(PersonaUpdate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        datos_iniciales = super(PersonaUpdate, self).get_initial()
        persona = Persona.objects.get(pk=self.object.id)
        datos_iniciales['grupo_familiar'] = persona.grupo_familiar.id
        datos_iniciales['edad'] = persona.edad
        return datos_iniciales

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if form.cleaned_data['tiene_cedula']=="S":
            self.object.cedula = form.cleaned_data['cedula']
        else:
            self.object.cedula = None
        self.object.save()
        return super(PersonaUpdate, self).form_valid(form)

    def form_invalid(self, form):
        return super(PersonaUpdate, self).form_invalid(form)

class PersonaDelete(DeleteView):
    model = Persona
    template_name = "persona.eliminar.html"
    success_url = reverse_lazy('persona_listar')

    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        if not Persona.objects.filter(pk=self.kwargs['pk'],grupo_familiar__street_leader__perfil__user=user):
            return redirect('base_403')
        return super(PersonaDelete, self).dispatch(request, *args, **kwargs)
