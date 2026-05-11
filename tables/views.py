from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Table
from commandes.models import Commande

def choisir_table(request):
    # Récupérer les IDs des tables avec commande en cours
    tables_occupees_ids = Commande.objects.filter(
        statut__in=['en_attente', 'en_preparation', 'prete', 'servie']
    ).values_list('table_id', flat=True)
    
    # Récupérer toutes les tables avec leur statut
    all_tables = Table.objects.all()
    
    # Ajouter l'attribut est_occupee à chaque table
    for table in all_tables:
        table.est_occupee = table.id in tables_occupees_ids
    
    if request.method == 'POST':
        table_id = request.POST.get('table_id')
        table = get_object_or_404(Table, id=table_id)
        
        # Vérifier si la table est déjà occupée
        commande_existante = Commande.objects.filter(
            table=table,
            statut__in=['en_attente', 'en_preparation', 'prete', 'servie']
        ).exists()
        
        if commande_existante:
            messages.error(request, f'❌ La table {table.numero} est déjà occupée')
            return redirect('choisir_table')
        
        request.session['table_id'] = table.id
        messages.success(request, f'✅ Table {table.numero} réservée')
        return redirect('menu')
    
    return render(request, 'tables/choisir_table.html', {
        'tables': all_tables
    })