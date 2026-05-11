from django.db import models
from commandes.models import Commande

class Paiement(models.Model):
    MODE_CHOICES = [
        ('especes', 'Espèces'),
        ('carte', 'Carte bancaire'),
        ('mobile', 'Paiement mobile'),
    ]
    
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Paiement {self.id} - {self.montant}€"
    
    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"