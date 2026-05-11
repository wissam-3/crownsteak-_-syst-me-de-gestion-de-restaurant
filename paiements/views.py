from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from commandes.models import Commande
from .models import Paiement

def demande_facture(request, commande_id):
    """Client demande la facture pour sa commande"""
    commande = get_object_or_404(Commande, id=commande_id)
    
    if request.method == 'POST':
        return redirect('facture', commande_id=commande.id)
    
    return render(request, 'paiements/demande_facture.html', {'commande': commande})

def facture(request, commande_id):
    """Affiche la facture de la commande (client)"""
    commande = get_object_or_404(Commande, id=commande_id)
    return render(request, 'paiements/facture.html', {'commande': commande})


# ========== DASHBOARD CAISSIER ==========
@login_required
def caissier_dashboard(request):
    """Dashboard pour le caissier - voit les commandes à encaisser"""
    
    if not request.user.groups.filter(name='caissier').exists() and not request.user.is_superuser:
        messages.error(request, 'Accès non autorisé')
        return redirect('accueil')
    
    commandes_a_payer = Commande.objects.filter(statut='servie').order_by('date')
    
    if request.method == 'POST':
        commande_id = request.POST.get('commande_id')
        return redirect('paiement_caissier', commande_id=commande_id)
    
    return render(request, 'paiements/caissier_dashboard.html', {
        'commandes': commandes_a_payer
    })


def paiement_caissier(request, commande_id):
    """Formulaire de paiement pour le caissier"""
    commande = get_object_or_404(Commande, id=commande_id)
    
    if request.method == 'POST':
        mode = request.POST.get('mode')
        
        if not mode:
            messages.error(request, 'Veuillez sélectionner un mode de paiement')
            return redirect('paiement_caissier', commande_id=commande.id)
        
        # Enregistrer le paiement
        Paiement.objects.create(
            commande=commande,
            montant=commande.total,
            mode=mode
        )
        commande.statut = 'payee'
        commande.save()
        
        messages.success(request, f'✅ Paiement de {commande.total}€ effectué pour la table {commande.table.numero}')
        
        # Le caissier retourne à son dashboard (pas à l'accueil)
        return redirect('caissier_dashboard')
    
    return render(request, 'paiements/paiement_caissier.html', {'commande': commande})