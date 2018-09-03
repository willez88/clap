from django.contrib import admin
from .models import Clap, Sex, MaritalStatus, FamilyRelationship
from .forms import ClapAdminForm

class ClapAdmin(admin.ModelAdmin):
    form = ClapAdminForm
    change_form_template = 'base/admin/change_form.html'
    list_display = ('code','name','parish',)
    list_filter = ('parish',)
    ordering = ('parish',)
    
admin.site.register(Clap, ClapAdmin)


class SexAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

admin.site.register(Sex, SexAdmin)

class MaritalStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

admin.site.register(MaritalStatus, MaritalStatusAdmin)

class FamilyRelationshipAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

admin.site.register(FamilyRelationship, FamilyRelationshipAdmin)