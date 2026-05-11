from django.db import models

class Table(models.Model):
    numero = models.IntegerField(unique=True, verbose_name="Numéro de table")
    est_libre = models.BooleanField(default=True, verbose_name="Table libre")
    
    def __str__(self):
        return f"Table {self.numero}"