from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import FamilyGroup, Person
from user.models import StreetLeader
from .forms import PersonForm
from django.contrib.auth.models import User
from user.models import ClapLevel

class PersonListView(ListView):
    model = Person
    template_name = 'person.list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 6 or self.request.user.profile.level == 7:
            return super(PersonListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_queryset(self):

        if StreetLeader.objects.filter(profile=self.request.user.profile):
            street_leader = StreetLeader.objects.get(profile=self.request.user.profile)
            queryset = Person.objects.filter(family_group__street_leader__clap_level__clap=street_leader.clap_level.clap)
            return queryset

        if FamilyGroup.objects.filter(profile=self.request.user.profile):
            family_group = FamilyGroup.objects.get(profile=self.request.user.profile)
            queryset = Person.objects.filter(family_group=family_group)
            return queryset

class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'person.create.html'
    success_url = reverse_lazy('person_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 6:
            return super(PersonCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_form_kwargs(self):
        kwargs = super(PersonCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        family_group = FamilyGroup.objects.get(pk=form.cleaned_data['family_group'])
        self.object = form.save(commit=False)
        self.object.family_group = family_group
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        if form.cleaned_data['has_identity_card']=='S':
            self.object.identity_card = form.cleaned_data['identity_card']
        else:
            self.object.identity_card = None
        self.object.phono = form.cleaned_data['phono']
        self.object.email = form.cleaned_data['email']
        self.object.sex = form.cleaned_data['sex']
        self.object.birthdate = form.cleaned_data['birthdate']
        self.object.family_relationship = form.cleaned_data['family_relationship']
        if form.cleaned_data['family_head']:
            self.object.family_head = form.cleaned_data['family_head']
        self.object.marital_status = form.cleaned_data['marital_status']
        self.object.observation = form.cleaned_data['observation']
        self.object.save()
        return super(PersonCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(PersonCreateView, self).form_invalid(form)

class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'person.create.html'
    success_url = reverse_lazy('person_list')

    def get_form_kwargs(self):
        kwargs = super(PersonUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        if not Person.objects.filter(pk=self.kwargs['pk'],family_group__street_leader__profile__user=user):
            return redirect('base_403')
        return super(PersonUpdateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial_data = super(PersonUpdateView, self).get_initial()
        person = Person.objects.get(pk=self.object.id)
        initial_data['family_group'] = person.family_group.id
        initial_data['age'] = person.age
        return initial_data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if form.cleaned_data['has_identity_card']=='S':
            self.object.identity_card = form.cleaned_data['identity_card']
        else:
            self.object.identity_card = None
        self.object.save()
        return super(PersonUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(PersonUpdateView, self).form_invalid(form)

class PersonDeleteView(DeleteView):
    model = Person
    template_name = 'person.update.html'
    success_url = reverse_lazy('person_list')

    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        if not Person.objects.filter(pk=self.kwargs['pk'],family_group__street_leader__profile__user=user):
            return redirect('base_403')
        return super(PersonDeleteView, self).dispatch(request, *args, **kwargs)
