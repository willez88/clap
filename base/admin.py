from django.contrib import admin
from .models import Clap
from .forms import ClapAdminForm

class ClapAdmin(admin.ModelAdmin):
    form = ClapAdminForm
    change_form_template = 'base/admin/change_form.html'
    list_display = ('code','name','parish',)
    list_filter = ('parish',)
    #list_per_page = 25
    ordering = ('parish',)
    #search_fields = ('codigo','nombre','parroquia',)

## Registra el modelo ConsejoComunal en el panel administrativo
admin.site.register(Clap, ClapAdmin)
