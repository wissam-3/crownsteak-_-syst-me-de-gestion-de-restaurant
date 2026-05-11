from django.contrib import admin
from .models import Plat, PlatImage

class PlatImageInline(admin.TabularInline):
    model = PlatImage
    extra = 3
    fields = ['image', 'is_principal']

@admin.register(Plat)
class PlatAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prix', 'categorie', 'disponible']
    list_editable = ['prix', 'disponible']
    list_filter = ['categorie', 'disponible']
    search_fields = ['nom']
    inlines = [PlatImageInline]

@admin.register(PlatImage)
class PlatImageAdmin(admin.ModelAdmin):
    list_display = ['plat', 'is_principal']
    list_filter = ['is_principal']