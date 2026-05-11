from django.contrib import admin
from .models import Paiement

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ['commande', 'montant', 'mode', 'date']
    list_filter = ['mode', 'date']