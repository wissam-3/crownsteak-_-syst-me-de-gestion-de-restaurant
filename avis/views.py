from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Avis

def avis(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        note = request.POST.get('note')
        commentaire = request.POST.get('commentaire')
        
        if nom and note and commentaire:
            Avis.objects.create(
                nom=nom,
                note=note,
                commentaire=commentaire,
                approuve=False
            )
            messages.success(request, 'Merci pour votre avis ! Il sera publié après validation.')
            return redirect('avis')
        else:
            messages.error(request, 'Veuillez remplir tous les champs')
    
    # Afficher les avis approuvés
    avis_approuves = Avis.objects.filter(approuve=True).order_by('-date')[:6]
    
    return render(request, 'avis/avis.html', {
        'avis_list': avis_approuves,
        'notes': dict(Avis.NOTE_CHOICES)
    })