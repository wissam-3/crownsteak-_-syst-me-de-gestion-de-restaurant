from django.contrib import admin
from .models import Commande, LigneCommande

class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 1

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['id', 'table', 'date', 'statut', 'total']
    list_filter = ['statut', 'date']
    search_fields = ['table__numero']
    inlines = [LigneCommandeInline]