from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tables.models import Table
from plats.models import Plat
from .models import Commande, LigneCommande

# ========== VALIDER LA COMMANDE ==========
def valider_commande(request):
    panier = request.session.get('panier', {})
    table_id = request.session.get('table_id')
    
    if not table_id:
        messages.warning(request, 'Veuillez d\'abord choisir une table')
        return redirect('choisir_table')
    
    table = get_object_or_404(Table, id=table_id)
    
    if not panier:
        messages.warning(request, 'Votre panier est vide')
        return redirect('menu')
    
    if request.method == 'POST':
        commande = Commande.objects.create(table=table, statut='en_attente')
        
        for plat_id, quantite in panier.items():
            plat = Plat.objects.get(id=plat_id)
            LigneCommande.objects.create(commande=commande, plat=plat, quantite=quantite)
        
        commande.calculer_total()
        request.session['commande_id'] = commande.id
        del request.session['panier']
        
        messages.success(request, f'Commande #{commande.id} validée !')
        return redirect('suivi_commande', commande_id=commande.id)
    
    plats_panier = []
    total = 0
    for plat_id, quantite in panier.items():
        plat = Plat.objects.get(id=plat_id)
        sous_total = float(plat.prix) * int(quantite)
        total += sous_total
        plats_panier.append({'plat': plat, 'quantite': int(quantite), 'total': sous_total})
    
    return render(request, 'commandes/valider_commande.html', {
        'plats': plats_panier, 
        'total': total, 
        'table': table
    })


# ========== SUIVI COMMANDE CLIENT ==========
def suivi_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    
    status_labels = {
        'en_attente': ('warning', '⏳', 'En attente du chef'),
        'en_preparation': ('info', '🍳', 'En cours de préparation'),
        'prete': ('success', '✅', 'Commande prête !'),
        'servie': ('secondary', '🍽️', 'Commandes servie'),
        'payee': ('success', '💳', 'Payée - Merci !'),
    }
    
    context = {
        'commande': commande,
        'status_class': status_labels.get(commande.statut, ('secondary', '❓', ''))[0],
        'status_icon': status_labels.get(commande.statut, ('secondary', '❓', ''))[1],
        'status_text': status_labels.get(commande.statut, ('secondary', '❓', ''))[2],
    }
    
    return render(request, 'commandes/suivi_commande.html', context)


# ========== DASHBOARD CHEF ==========
@login_required
def chef_dashboard(request):
    # Vérifier si l'utilisateur est chef
    if not request.user.groups.filter(name='chef').exists() and not request.user.is_superuser:
        messages.error(request, 'Accès non autorisé')
        return redirect('accueil')
    
    commandes_attente = Commande.objects.filter(statut='en_attente').order_by('date')
    commandes_preparation = Commande.objects.filter(statut='en_preparation').order_by('date')
    
    if request.method == 'POST':
        commande_id = request.POST.get('commande_id')
        action = request.POST.get('action')
        
        try:
            commande = Commande.objects.get(id=commande_id)
            if action == 'preparer' and commande.statut == 'en_attente':
                commande.statut = 'en_preparation'
                commande.save()
                messages.success(request, f'✅ Commande #{commande_id} : en préparation')
            elif action == 'prete' and commande.statut == 'en_preparation':
                commande.statut = 'prete'
                commande.save()
                messages.success(request, f'✅ Commande #{commande_id} : prête !')
        except Commande.DoesNotExist:
            messages.error(request, 'Commande introuvable')
        
        return redirect('chef_dashboard')
    
    return render(request, 'commandes/chef_dashboard.html', {
        'commandes_attente': commandes_attente,
        'commandes_preparation': commandes_preparation,
    })

# ========== DASHBOARD SERVEUR ==========
@login_required
def serveur_dashboard(request):
    # Vérifier si l'utilisateur est serveur
    if not request.user.groups.filter(name='serveur').exists() and not request.user.is_superuser:
        messages.error(request, 'Accès non autorisé')
        return redirect('accueil')
    
    commandes_prete = Commande.objects.filter(statut='prete').order_by('date')
    
    if request.method == 'POST':
        commande_id = request.POST.get('commande_id')
        
        try:
            commande = Commande.objects.get(id=commande_id)
            if commande.statut == 'prete':
                commande.statut = 'servie'
                commande.save()
                messages.success(request, f'Commande #{commande_id} - Table {commande.table.numero} servie')
            else:
                messages.warning(request, f'Commande #{commande_id} non prête')
        except Commande.DoesNotExist:
            messages.error(request, 'Commande introuvable')
        
        return redirect('serveur_dashboard')
    
    return render(request, 'commandes/serveur_dashboard.html', {
        'commandes': commandes_prete
    })


# ========== DASHBOARD CAISSIER ==========
@login_required
def caissier_dashboard(request):
    # Vérifier si l'utilisateur est caissier
    if not request.user.groups.filter(name='caissier').exists() and not request.user.is_superuser:
        messages.error(request, 'Accès non autorisé')
        return redirect('accueil')
    
    # Commandes servies (prêtes à être payées)
    commandes_a_payer = Commande.objects.filter(statut='servie').order_by('date')
    
    if request.method == 'POST':
        commande_id = request.POST.get('commande_id')
        
        try:
            commande = Commande.objects.get(id=commande_id)
            if commande.statut == 'servie':
                commande.statut = 'payee'
                commande.save()
                messages.success(request, f'Commande #{commande_id} - Table {commande.table.numero} payée')
            else:
                messages.warning(request, f'Commande #{commande_id} non payable')
        except Commande.DoesNotExist:
            messages.error(request, 'Commande introuvable')
        
        return redirect('caissier_dashboard')
    
    return render(request, 'paiements/caissier_dashboard.html', {
        'commandes': commandes_a_payer
    })

# ========== SUIVI COMMANDE SANS ID (UTILISE LA SESSION) ==========
def suivi_commande_session(request):
    """Affiche la commande en cours du client sans avoir à mettre l'ID"""
    
    commande_id = request.session.get('commande_id')
    table_id = request.session.get('table_id')
    
    if not commande_id or not table_id:
        messages.warning(request, 'Aucune commande en cours')
        return redirect('choisir_table')
    
    try:
        commande = Commande.objects.get(id=commande_id, table_id=table_id)
    except Commande.DoesNotExist:
        messages.warning(request, 'Commande introuvable')
        return redirect('choisir_table')
    
    status_labels = {
        'en_attente': ('warning', '⏳', 'En attente du chef'),
        'en_preparation': ('info', '🍳', 'En cours de préparation'),
        'prete': ('success', '✅', 'Commande prête !'),
        'servie': ('secondary', '🍽️', 'Commande servie'),
        'payee': ('success', '💳', 'Payée - Merci !'),
    }
    
    context = {
        'commande': commande,
        'status_class': status_labels.get(commande.statut, ('secondary', '❓', ''))[0],
        'status_icon': status_labels.get(commande.statut, ('secondary', '❓', ''))[1],
        'status_text': status_labels.get(commande.statut, ('secondary', '❓', ''))[2],
    }
    
    return render(request, 'commandes/suivi_commande.html', context)