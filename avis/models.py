from django.db import models

class Avis(models.Model):
    NOTE_CHOICES = [
        (1, '⭐ Très mauvais'),
        (2, '⭐⭐ Mauvais'),
        (3, '⭐⭐⭐ Moyen'),
        (4, '⭐⭐⭐⭐ Bien'),
        (5, '⭐⭐⭐⭐⭐ Excellent'),
    ]
    
    nom = models.CharField(max_length=100, verbose_name="Votre nom")
    note = models.IntegerField(choices=NOTE_CHOICES, verbose_name="Note")
    commentaire = models.TextField(verbose_name="Votre avis")
    date = models.DateTimeField(auto_now_add=True)
    approuve = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.nom} - {self.note} étoiles"
    
    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis"