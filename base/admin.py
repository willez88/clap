from django.contrib import admin
from .models import Clap
from .forms import ClapAdminForm

class ClapAdmin(admin.ModelAdmin):
    form = ClapAdminForm
    change_form_template = 'change_form.html'
    list_display = ('codigo','nombre','parroquia',)
    list_filter = ('codigo','nombre','parroquia',)
    list_per_page = 25
    ordering = ('parroquia',)
    search_fields = ('codigo','nombre','parroquia',)

## Registra el modelo ConsejoComunal en el panel administrativo
admin.site.register(Clap, ClapAdmin)
