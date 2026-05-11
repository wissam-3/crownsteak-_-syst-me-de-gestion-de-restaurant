from django.contrib import admin
from .models import Table

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['numero', 'est_libre']
    list_editable = ['est_libre']
    list_filter = ['est_libre']
    search_fields = ['numero']