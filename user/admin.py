from django.contrib import admin
from .models import (
    Profile, NationalLevel, StateLevel, MunicipalityLevel, ParishLevel, ClapLevel,
    StreetLeader, FamilyGroup
)

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','level','phone',)
    list_filter = ('level',)
    ordering = ('user',)
admin.site.register(Profile, ProfileAdmin)

class NationalLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','country',)
    #list_filter = ('perfil','pais',)
    #list_per_page = 25
    ordering = ('country',)
admin.site.register(NationalLevel, NationalLevelAdmin)

class StateLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','state',)
    #list_filter = ('perfil','estado',)
    #list_per_page = 25
    ordering = ('state',)
admin.site.register(StateLevel, StateLevelAdmin)

class MunicipalityLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','municipality',)
    ordering = ('profile',)
admin.site.register(MunicipalityLevel, MunicipalityLevelAdmin)

class ParishLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','parish',)
    ordering = ('parish',)
admin.site.register(ParishLevel, ParishLevelAdmin)

class ClapLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','clap',)
    ordering = ('clap',)
admin.site.register(ClapLevel, ClapLevelAdmin)

class StreetLeaderAdmin(admin.ModelAdmin):
    list_display = ('profile','clap_level',)
    ordering = ('clap_level',)
admin.site.register(StreetLeader, StreetLeaderAdmin)

class FamilyGroupAdmin(admin.ModelAdmin):
    list_display = ('profile','street_leader',)
    ordering = ('street_leader',)
admin.site.register(FamilyGroup, FamilyGroupAdmin)
