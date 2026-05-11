from django.db import models

class Plat(models.Model):
    CATEGORIE_CHOICES = [
        ('entree', 'Entrée'),
        ('plat', 'Plat Principal'),
        ('dessert', 'Dessert'),
        ('boisson', 'Boisson'),
    ]
    
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    disponible = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nom} - {self.prix}€"

class PlatImage(models.Model):
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='plats/', blank=True, null=True)
    is_principal = models.BooleanField(default=False)
    order = models.IntegerField(default=0)  # Ajoutez ce champ
    
    def __str__(self):
        return f"Image de {self.plat.nom}"