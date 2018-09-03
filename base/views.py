from django.shortcuts import render
from django.views.generic import TemplateView
from user.models import (
    NationalLevel, StateLevel, MunicipalityLevel, ParishLevel, ClapLevel, StreetLeader,
    FamilyGroup
)

# Create your views here.

class HomeTemplateView(TemplateView):
    """!
    Clase para mostrar la página de inicio

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    """

    template_name = 'base/base.html'

    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        profile = self.request.user.profile
        if profile.level == 1:
            national_level = NationalLevel.objects.get(profile=profile)
            context['text1'] = 'Bienvenido ' + str(profile)
            context['text2'] = 'Usuario nivel nacional ' + str(national_level.country) + '. Este usuario permite registrar y monitorear a los representantes de \
            cada estado que pertenecen a dicho país'
        elif profile.level == 2:
            state_level = StateLevel.objects.get(profile=profile)
            context['text1'] = 'Bienvenido ' + str(profile)
            context['text2'] = 'Usuario nivel estado ' + str(state_level.state) + '. Este usuario permite registrar y monitorear a los representantes de \
            cada municipio que pertenecen a dicho estado'
        elif profile.level == 3:
            municipality_level = MunicipalityLevel.objects.get(profile=profile)
            context['text1'] = 'Bienvenido ' + str(profile)
            context['text2'] = 'Usuario nivel municipio ' + str(municipality_level.municipality) + '. Este usuario permite registrar y monitorear a los representantes \
            de cada parroquia que pertenecen a dicho municipio'
        elif profile.level == 4:
            parish_level = ParishLevel.objects.get(profile=profile)
            context['text1'] = 'Bienvenido ' + str(profile)
            context['text2'] = 'Usuario nivel parroquia ' + str(parish_level.parish) + '. Este usuario permite registrar y monitorear a los representantes \
            de cada clap que pertenecen a dicha parroquia'
        elif profile.level == 5:
            clap_level = ClapLevel.objects.get(profile=profile)
            context['text1'] = 'Bienvenido ' + str(profile)
            context['text2'] = 'Usuario nivel Clap ' + str(clap_level.clap) + '. Este usuario permite registrar y monitorear a los representantes \
            de cada clap que pertenecen a dicha parroquia'
        elif profile.level == 6:
            street_leader = StreetLeader.objects.get(profile=profile)
            context['text1'] = 'Bienvenido ' + str(profile)
            context['text2'] = 'Usuario nivel Líder de Calle perteneciente a' + str(street_leader.clap_level.clap) + '. Este usuario permite registrar y monitorear a \
            cada Líder de Calle que pertenecen a dicha parroquia'
        elif profile.level == 7:
            family_group = FamilyGroup.objects.get(profile=profile)
            context['text1'] = 'Bienvenido ' + str(profile)
            context['text2'] = 'Usuario nivel grupo familiar. Este usuario permite responder una encuesta acerca de la frecuencia con que le llega el clap'
        return context

class Error403TemplateView(TemplateView):
    """!
    Clase para mostrar error de permiso

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    """

    template_name = 'base.error.403.html'
