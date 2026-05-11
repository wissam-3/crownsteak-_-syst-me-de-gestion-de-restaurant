from django.db import models
from tables.models import Table
from plats.models import Plat

class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_preparation', 'En préparation'),
        ('prete', 'Prête'),
        ('servie', 'Servie'),
        ('payee', 'Payée'),
    ]
    
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def calculer_total(self):
        total = 0
        for ligne in self.lignecommande_set.all():
            total += float(ligne.plat.prix) * int(ligne.quantite)
        self.total = total
        self.save()
        return total
    
    def __str__(self):
        return f"Commande {self.id} - Table {self.table.numero}"


class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.plat.nom} x {self.quantite}"