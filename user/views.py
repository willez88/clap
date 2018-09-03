from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import (
    NationalLevelUpdateForm, StateLevelForm, StateLevelUpdateForm, MunicipalityLevelForm,
    ParishLevelForm, MunicipalityLevelUpdateForm, ParishLevelUpdateForm, ClapLevelForm,
    ClapLevelUpdateForm, ProfileForm, FamilyGroupUpdateForm, StreetLeaderUpdateForm
)
from .models import (
    Profile, NationalLevel, StateLevel, MunicipalityLevel, ParishLevel, ClapLevel,
    StreetLeader, FamilyGroup
)

from django.contrib.auth.models import User
from base.models import State, Municipality, Parish, Clap
from django.conf import settings
from base.constant import EMAIL_SUBJECT
from base.functions import send_email
from django.utils.translation import ugettext_lazy as _
import logging
logger = logging.getLogger('user')

# Create your views here.

class NationalLevelUpdateView(UpdateView):
    model = User
    form_class = NationalLevelUpdateForm
    template_name = 'user/national.level.update.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.profile.level == 1:
            return super(NationalLevelUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_initial(self):
        initial_data = super(NationalLevelUpdateView, self).get_initial()
        profile = Profile.objects.get(user=self.object)
        initial_data['phone'] = profile.phone
        national_level = NationalLevel.objects.get(profile=profile)
        initial_data['country'] = national_level.country
        return initial_data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Profile.objects.filter(user=self.object):
            profile = Profile.objects.get(user=self.object)
            profile.phone = form.cleaned_data['phone']
            profile.save()
        return super(NationalLevelUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(NationalLevelUpdateView, self).form_invalid(form)

class StateLevelListView(ListView):
    model = StateLevel
    template_name = 'user/state.level.list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 1:
            return super(StateLevelListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        ## usuario nacioanl puede ver al nivel estadal
        if NationalLevel.objects.filter(profile=self.request.user.profile):
            national_level = NationalLevel.objects.get(profile=self.request.user.profile)
            queryset = StateLevel.objects.filter(state__country=national_level.country)
            return queryset

class StateLevelCreateView(CreateView):
    model = User
    form_class = StateLevelForm
    template_name = 'user/state.level.create.html'
    success_url = reverse_lazy('user:state_level_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 1:
            return super(StateLevelCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super(StateLevelCreateView, self).get_form_kwargs()
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
        profile = Profile.objects.create(
            phone=form.cleaned_data['phone'],
            level = 2,
            user= user
        )

        state = State.objects.get(pk=form.cleaned_data['state'])
        StateLevel.objects.create(
            state = state,
            profile = profile
        )

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        sent = send_email(self.object.email, 'user/welcome.mail', EMAIL_SUBJECT, {'level':'Nacional','first_name':self.request.user.first_name,
            'last_name':self.request.user.last_name, 'email':self.request.user.email, 'username':self.object.username, 'password':form.cleaned_data['password'],
            'admin':admin, 'admin_email':admin_email, 'emailapp':settings.EMAIL_FROM
        })

        if not sent:
            logger.warning(
                str(_('Ocurrió un inconveniente al enviar por correo las credenciales del usuario [%s]') % self.object.username)
            )

        return super(StateLevelCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(StateLevelCreateView, self).form_invalid(form)

class StateLevelUpdateView(UpdateView):
    model = User
    form_class = StateLevelUpdateForm
    template_name = 'user/state.level.update.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.profile.level == 2:
            return super(StateLevelUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_initial(self):
        initial_data = super(StateLevelUpdateView, self).get_initial()
        profile = Profile.objects.get(user=self.object)
        initial_data['phone'] = profile.phone
        state_level = StateLevel.objects.get(profile=profile)
        initial_data['state'] = state_level.state
        return initial_data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Profile.objects.filter(user=self.object):
            profile = Profile.objects.get(user=self.object)
            profile.phone = form.cleaned_data['phone']
            profile.save()
        return super(StateLevelUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(StateLevelUpdateView, self).form_invalid(form)

class MunicipalityLevelListView(ListView):
    model = MunicipalityLevel
    template_name = 'user/municipality.level.list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 1 or self.request.user.profile.level == 2:
            return super(MunicipalityLevelListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        ## usuario nacional puede ver al nivel municipal
        if NationalLevel.objects.filter(profile=self.request.user.profile):
            national_level = NationalLevel.objects.get(profile=self.request.user.profile)
            queryset = MunicipalityLevel.objects.filter(municipality__state__country=national_level.country)
            return queryset

        ## usuario estadal puede ver al nivel municipal
        if StateLevel.objects.filter(profile=self.request.user.profile):
            state_level = StateLevel.objects.get(profile=self.request.user.profile)
            queryset = MunicipalityLevel.objects.filter(municipality__state=state_level.state)
            return queryset

class MunicipalityLevelCreateView(CreateView):
    model = User
    form_class = MunicipalityLevelForm
    template_name = 'user/municipality.level.create.html'
    success_url = reverse_lazy('user:municipality_level_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 2:
            return super(MunicipalityLevelCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super(MunicipalityLevelCreateView, self).get_form_kwargs()
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
        profile = Profile.objects.create(
            phone = form.cleaned_data['phone'],
            level = 3,
            user= user
        )

        municipality = Municipality.objects.get(pk=form.cleaned_data['municipality'])
        MunicipalityLevel.objects.create(
            municipality = municipality,
            profile = profile
        )

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        sent = send_email(self.object.email, 'user/welcome.mail', EMAIL_SUBJECT, {'level':'Estadal','first_name':self.request.user.first_name,
            'last_name':self.request.user.last_name, 'email':self.request.user.email, 'username':self.object.username, 'password':form.cleaned_data['password'],
            'admin':admin, 'admin_email':admin_email, 'emailapp':settings.EMAIL_FROM
        })

        if not sent:
            logger.warning(
                str(_('Ocurrió un inconveniente al enviar por correo las credenciales del usuario [%s]') % self.object.username)
            )

        return super(MunicipalityLevelCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(MunicipalityLevelCreateView, self).form_invalid(form)

class MunicipalityLevelUpdateView(UpdateView):
    model = User
    form_class = MunicipalityLevelUpdateForm
    template_name = 'user/municipality.level.update.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.profile.level == 3:
            return super(MunicipalityLevelUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_form_kwargs(self):
        kwargs = super(MunicipalityLevelUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        initial_data = super(MunicipalityLevelUpdateView, self).get_initial()
        profile = Profile.objects.get(user=self.object)
        initial_data['phone'] = profile.phone
        municipality_level = MunicipalityLevel.objects.get(profile=profile)
        initial_data['municipality'] = municipality_level.municipality
        return initial_data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Profile.objects.filter(user=self.object):
            profile = Profile.objects.get(user=self.object)
            profile.phone = form.cleaned_data['phone']
            profile.save()
        return super(MunicipalityLevelUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(MunicipalityLevelUpdateView, self).form_invalid(form)

class ParishLevelListView(ListView):
    model = ParishLevel
    template_name = 'user/parish.level.list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 1 or self.request.user.profile.level == 2 or self.request.user.profile.level == 3:
            return super(ParishLevelListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        ## usuario nacional puede ver al nivel parroquial
        if NationalLevel.objects.filter(profile=self.request.user.profile):
            national_level = NationalLevel.objects.get(profile=self.request.user.profile)
            queryset = ParishLevel.objects.filter(parish__municipality__state__country=national_level.country)
            return queryset

        ## usuario estadal puede ver al nivel parroquial
        if StateLevel.objects.filter(profile=self.request.user.profile):
            state_level = StateLevel.objects.get(profile=self.request.user.profile)
            queryset = ParishLevel.objects.filter(parish__municipality__state=state_level.state)
            return queryset

        ## usuario municipal puede ver al parroquial
        if MunicipalityLevel.objects.filter(profile=self.request.user.profile):
            municipality_level = MunicipalityLevel.objects.get(profile=self.request.user.profile)
            queryset = ParishLevel.objects.filter(parish__municipality=municipality_level.municipality)
            return queryset

class ParishLevelCreateView(CreateView):
    model = User
    form_class = ParishLevelForm
    template_name = 'user/parish.level.create.html'
    success_url = reverse_lazy('user:parish_level_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 3:
            return super(ParishLevelCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super(ParishLevelCreateView, self).get_form_kwargs()
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
        profile = Profile.objects.create(
            phone = form.cleaned_data['phone'],
            level = 4,
            user= user
        )

        parish = Parish.objects.get(pk=form.cleaned_data['parish'])
        ParishLevel.objects.create(
            parish = parish,
            profile = profile
        )

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        sent = send_email(self.object.email, 'user/welcome.mail', EMAIL_SUBJECT, {'level':'Municipal','first_name':self.request.user.first_name,
            'last_name':self.request.user.last_name, 'email':self.request.user.email, 'username':self.object.username, 'password':form.cleaned_data['password'],
            'admin':admin, 'admin_email':admin_email, 'emailapp':settings.EMAIL_FROM
        })

        if not sent:
            logger.warning(
                str(_('Ocurrió un inconveniente al enviar por correo las credenciales del usuario [%s]') % self.object.username)
            )

        return super(ParishLevelCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(ParishLevelCreateView, self).form_invalid(form)

class ParishLevelUpdateView(UpdateView):
    model = User
    form_class = ParishLevelUpdateForm
    template_name = 'user/parish.level.update.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.profile.level == 4:
            return super(ParishLevelUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super(ParishLevelUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        initial_data = super(ParishLevelUpdateView, self).get_initial()
        profile = Profile.objects.get(user=self.object)
        initial_data['phone'] = profile.phone
        parish_level = ParishLevel.objects.get(profile=profile)
        initial_data['parish'] = parish_level.parish
        return initial_data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Profile.objects.filter(user=self.object):
            profile = Profile.objects.get(user=self.object)
            profile.phone = form.cleaned_data['phone']
            profile.save()
        return super(ParishLevelUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(ParishLevelUpdateView, self).form_invalid(form)

class ClapLevelListView(ListView):
    model = ClapLevel
    template_name = 'user/clap.level.list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 1 or self.request.user.profile.level == 2 or self.request.user.profile.level == 3 or self.request.user.profile.level == 4:
            return super(ClapLevelListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        ## usuario nacional puede ver al nivel comunal
        if NationalLevel.objects.filter(profile=self.request.user.profile):
            national_level = NationalLevel.objects.get(profile=self.request.user.profile)
            queryset = ClapLevel.objects.filter(clap__parish__municipality__state__country=national_level.country)
            return queryset

        ## usuario estadal puede ver al nivel comunal
        if StateLevel.objects.filter(profile=self.request.user.profile):
            state_level = StateLevel.objects.get(profile=self.request.user.profile)
            queryset = ClapLevel.objects.filter(clap__parish__municipality__state=state_level.state)
            return queryset

        ## usuario municipal puede ver al comunal
        if MunicipalityLevel.objects.filter(profile=self.request.user.profile):
            municipality_level = MunicipalityLevel.objects.get(profile=self.request.user.profile)
            queryset = ClapLevel.objects.filter(clap__parish__municipality=municipality_level.municipality)
            return queryset

        ## usuario parroquial puede ver al comunal
        if ParishLevel.objects.filter(profile=self.request.user.profile):
            parish_level = ParishLevel.objects.get(profile=self.request.user.profile)
            queryset = ClapLevel.objects.filter(clap__parish=parish_level.parish)
            return queryset

class ClapLevelCreateView(CreateView):
    model = User
    form_class = ClapLevelForm
    template_name = 'user/clap.level.create.html'
    success_url = reverse_lazy('user:clap_level_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 4:
            return super(ClapLevelCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super(ClapLevelCreateView, self).get_form_kwargs()
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
        profile = Profile.objects.create(
            phone = form.cleaned_data['phone'],
            level = 5,
            user= user
        )

        clap = Clap.objects.get(pk=form.cleaned_data['clap'])
        ClapLevel.objects.create(
            clap = clap,
            profile = profile
        )

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        sent = send_email(self.object.email, 'user/welcome.mail', EMAIL_SUBJECT, {'level':'Parroquial','first_name':self.request.user.first_name,
            'last_name':self.request.user.last_name, 'email':self.request.user.email, 'username':self.object.username, 'password':form.cleaned_data['password'],
            'admin':admin, 'admin_email':admin_email, 'emailapp':settings.EMAIL_FROM
        })

        if not sent:
            logger.warning(
                str(_('Ocurrió un inconveniente al enviar por correo las credenciales del usuario [%s]') % self.object.username)
            )

        return super(ClapLevelCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(ClapLevelCreateView, self).form_invalid(form)

class ClapLevelUpdateView(UpdateView):
    model = User
    form_class = ClapLevelUpdateForm
    template_name = 'user/clap.level.update.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.profile.level == 5:
            return super(ClapLevelUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super(ClapLevelUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        initial_data = super(ClapLevelUpdateView, self).get_initial()
        profile = Profile.objects.get(user=self.object)
        initial_data['phone'] = profile.phone
        clap_level = ClapLevel.objects.get(profile=profile)
        initial_data['clap'] = clap_level.clap
        return initial_data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Profile.objects.filter(user=self.object):
            profile = Profile.objects.get(user=self.object)
            profile.phone = form.cleaned_data['phone']
            profile.save()
        return super(ClapLevelUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(ClapLevelUpdateView, self).form_invalid(form)

class StreetLeaderListView(ListView):
    model = StreetLeader
    template_name = 'user/street.leader.list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 1 or self.request.user.profile.level == 2 or self.request.user.profile.level == 3 or self.request.user.profile.level == 4 or self.request.user.profile.level == 5:
            return super(StreetLeaderListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        ## usuario nacional puede ver al nivel comunal
        if NationalLevel.objects.filter(profile=self.request.user.profile):
            national_level = Nacional.objects.get(profile=self.request.user.profile)
            queryset = StreetLeader.objects.filter(clap_level__clap__parish__municipality__state__country=national_level.country)
            return queryset

        ## usuario estadal puede ver al nivel comunal
        if StateLevel.objects.filter(profile=self.request.user.profile):
            state_level = StateLevel.objects.get(profile=self.request.user.profile)
            queryset = StreetLeader.objects.filter(clap_level__clap__parish__municipality__state=state_level.state)
            return queryset

        ## usuario municipal puede ver al comunal
        if MunicipalityLevel.objects.filter(profile=self.request.user.profile):
            municipality_level = MunicipalityLevel.objects.get(profile=self.request.user.profile)
            queryset = StreetLeader.objects.filter(clap_level__clap__parish__municipality=municipality_level.municipality)
            return queryset

        ## usuario parroquial puede ver al comunal
        if ParishLevel.objects.filter(profile=self.request.user.profile):
            parish_level = ParishLevel.objects.get(profile=self.request.user.profile)
            queryset = StreetLeader.objects.filter(clap_level__clap__parish=parish_level.parish)
            return queryset

        ## usuario clap puede ver al líder de calle
        if ClapLevel.objects.filter(profile=self.request.user.profile):
            clap_level = ClapLevel.objects.get(profile=self.request.user.profile)
            queryset = StreetLeader.objects.filter(clap_level__clap=clap_level.clap)
            return queryset

class StreetLeaderCreateView(CreateView):
    model = User
    form_class = ProfileForm
    template_name = 'user/street.leader.create.html'
    success_url = reverse_lazy('user:street_leader_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 5:
            return super(StreetLeaderCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

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
        profile = Profile.objects.create(
            phone = form.cleaned_data['phone'],
            level = 6,
            user= user
        )

        clap_level = ClapLevel.objects.get(profile=self.request.user.profile)
        StreetLeader.objects.create(
            clap_level = clap_level,
            profile = profile
        )

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        sent = send_email(self.object.email, 'user/welcome.mail', EMAIL_SUBJECT, {'level':'Clap','first_name':self.request.user.first_name,
            'last_name':self.request.user.last_name, 'email':self.request.user.email, 'username':self.object.username, 'password':form.cleaned_data['password'],
            'admin':admin, 'admin_email':admin_email, 'emailapp':settings.EMAIL_FROM
        })

        if not sent:
            logger.warning(
                str(_('Ocurrió un inconveniente al enviar por correo las credenciales del usuario [%s]') % self.object.username)
            )

        return super(StreetLeaderCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(StreetLeaderCreateView, self).form_invalid(form)

class StreetLeaderUpdateView(UpdateView):
    model = User
    form_class = StreetLeaderUpdateForm
    template_name = 'user/street.leader.update.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.profile.level == 6:
            return super(StreetLeaderUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_initial(self):
        initial_data = super(StreetLeaderUpdateView, self).get_initial()
        profile = Profile.objects.get(user=self.object)
        initial_data['phone'] = profile.phone
        stree_leader = StreetLeader.objects.get(profile=profile)
        initial_data['clap'] = stree_leader.clap_level.clap
        return initial_data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Profile.objects.filter(user=self.object):
            profile = Profile.objects.get(user=self.object)
            profile.phone = form.cleaned_data['phone']
            profile.save()
        return super(StreetLeaderUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(StreetLeaderUpdateView, self).form_invalid(form)

class FamilyGroupListView(ListView):
    model = Profile
    template_name = 'user/family.group.list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 1 or self.request.user.profile.level == 2 or self.request.user.profile.level == 3 or self.request.user.profile.level == 4 or self.request.user.profile.level == 5 or self.request.user.profile.level == 6:
            return super(FamilyGroupListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        ## usuario nacional puede ver al nivel comunal
        if NationalLevel.objects.filter(profile=self.request.user.profile):
            national_levelional = NationalLevelional.objects.get(profile=self.request.user.profile)
            queryset = FamilyGroup.objects.filter(street_leader__clap_level__clap__parish__municipality__state__country=national_level.country)
            return queryset

        ## usuario estadal puede ver al nivel comunal
        if StateLevel.objects.filter(profile=self.request.user.profile):
            state_level = StateLevel.objects.get(profile=self.request.user.profile)
            queryset = FamilyGroup.objects.filter(street_leader__clap_level__clap__parish__municipality__state=state_level.state)
            return queryset

        ## usuario municipal puede ver al comunal
        if MunicipalityLevel.objects.filter(profile=self.request.user.profile):
            municipality_level = MunicipalityLevel.objects.get(profile=self.request.user.profile)
            queryset = FamilyGroup.objects.filter(street_leader__clap_level__clap__parish__municipality=municipality_level.municipality)
            return queryset

        ## usuario parroquial puede ver al comunal
        if ParishLevel.objects.filter(profile=self.request.user.profile):
            parish_level = ParishLevel.objects.get(profile=self.request.user.profile)
            queryset = FamilyGroup.objects.filter(street_leader__clap_level__clap__parish=parish_level.parish)
            return queryset

        if ClapLevel.objects.filter(profile=self.request.user.profile):
            clap_level = ClapLevel.objects.get(profile=self.request.user.profile)
            queryset = GrupoFamiliar.objects.filter(street_leader__clap_level__clap=clap_level.clap)
            return queryset

        if StreetLeader.objects.filter(profile=self.request.user.profile):
            street_leader = StreetLeader.objects.get(profile=self.request.user.profile)
            queryset = FamilyGroup.objects.filter(street_leader__clap_level__clap=street_leader.clap_level.clap)
            return queryset

class FamilyGroupCreateView(CreateView):
    model = User
    form_class = ProfileForm
    template_name = 'user/family.group.create.html'
    success_url = reverse_lazy('user:family_group_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 6:
            return super(FamilyGroupCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

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
        profile = Profile.objects.create(
            phone = form.cleaned_data['phone'],
            level = 7,
            user= user
        )

        street_leader = StreetLeader.objects.get(profile=self.request.user.profile)
        FamilyGroup.objects.create(
            street_leader = street_leader,
            profile = profile
        )

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        sent = send_email(self.object.email, 'user/welcome.mail', EMAIL_SUBJECT, {'level':'Jefe de calle','first_name':self.request.user.first_name,
            'last_name':self.request.user.last_name, 'email':self.request.user.email, 'username':self.object.username, 'password':form.cleaned_data['password'],
            'admin':admin, 'admin_email':admin_email, 'emailapp':settings.EMAIL_FROM
        })

        if not sent:
            logger.warning(
                str(_('Ocurrió un inconveniente al enviar por correo las credenciales del usuario [%s]') % self.object.username)
            )

        return super(FamilyGroupCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(FamilyGroupCreateView, self).form_invalid(form)

class FamilyGroupUpdateView(UpdateView):
    model = User
    form_class = FamilyGroupUpdateForm
    template_name = 'user/family.group.update.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.profile.level == 7:
            return super(FamilyGroupUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_initial(self):
        initial_data = super(FamilyGroupUpdateView, self).get_initial()
        profile = Profile.objects.get(user=self.object)
        initial_data['phone'] = profile.phone
        family_group = FamilyGroup.objects.get(profile=profile)
        initial_data['street_leader'] = family_group.street_leader
        return initial_data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Profile.objects.filter(user=self.object):
            profile = Profile.objects.get(user=self.object)
            profile.phone = form.cleaned_data['phone']
            profile.save()

        return super(FamilyGroupUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(FamilyGroupUpdateView, self).form_invalid(form)
