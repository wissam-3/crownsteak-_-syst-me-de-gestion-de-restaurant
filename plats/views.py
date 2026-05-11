from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Plat, PlatImage

def menu(request):
    plats = Plat.objects.filter(disponible=True)
    categorie_filter = request.GET.get('categorie')
    
    if categorie_filter:
        plats = plats.filter(categorie=categorie_filter)
    
    categories = dict(Plat.CATEGORIE_CHOICES)
    
    # Récupérer le panier
    panier = request.session.get('panier', {})
    
    if request.method == 'POST':
        plat_id = request.POST.get('plat_id')
        quantite = int(request.POST.get('quantite', 1))
        
        if plat_id in panier:
            panier[plat_id] += quantite
        else:
            panier[plat_id] = quantite
        
        request.session['panier'] = panier
        return redirect('menu')
    
    return render(request, 'plats/menu.html', {
        'plats': plats,
        'categories': categories,
        'categorie_active': categorie_filter,
        'panier': panier
    })

def detail_plat(request, plat_id):
    plat = get_object_or_404(Plat, id=plat_id)
    images = plat.images.all()
    image_principale = images.filter(is_principal=True).first() or images.first()
    
    if request.method == 'POST':
        quantite = int(request.POST.get('quantite', 1))
        panier = request.session.get('panier', {})
        panier[str(plat_id)] = panier.get(str(plat_id), 0) + quantite
        request.session['panier'] = panier
        return redirect('panier')
    
    return render(request, 'plats/detail_plat.html', {
        'plat': plat,
        'images': images,
        'image_principale': image_principale
    })

def panier(request):
    panier = request.session.get('panier', {})
    details_panier = []
    total = 0
    
    for plat_id, quantite in panier.items():
        plat = Plat.objects.get(id=plat_id)
        sous_total = plat.prix * quantite
        total += sous_total
        details_panier.append({
            'plat': plat,
            'quantite': quantite,
            'sous_total': sous_total
        })
    
    if request.method == 'POST':
        # Supprimer un article
        if 'supprimer' in request.POST:
            plat_id = request.POST.get('plat_id')
            if plat_id in panier:
                del panier[plat_id]
                request.session['panier'] = panier
                return redirect('panier')
        
        # Modifier la quantité
        if 'modifier_qte' in request.POST:
            plat_id = request.POST.get('plat_id')
            quantite = int(request.POST.get('quantite', 1))
            if quantite <= 0:
                del panier[plat_id]
            else:
                panier[plat_id] = quantite
            request.session['panier'] = panier
            return redirect('panier')
        
        # Vider le panier
        if 'vider' in request.POST:
            request.session['panier'] = {}
            return redirect('menu')
    
    return render(request, 'plats/panier.html', {
        'panier_items': details_panier,
        'total': total
    })