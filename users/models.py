from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = [
        ('serveur', 'Serveur'),
        ('chef', 'Chef'),
        ('caissier', 'Caissier'),
        ('admin', 'Administrateur'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='serveur')
    telephone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

# Signal pour ajouter automatiquement l'utilisateur au groupe correspondant
@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        # Ne rien faire, l'admin choisira le groupe manuellement
        pass

@receiver(post_save, sender=Profile)
def update_user_group(sender, instance, **kwargs):
    """Met à jour le groupe de l'utilisateur selon son rôle"""
    from django.contrib.auth.models import Group
    
    # Récupérer ou créer les groupes
    group_map = {
        'serveur': 'serveur',
        'chef': 'chef', 
        'caissier': 'caissier',
        'admin': 'admin'
    }
    
    if instance.role in group_map:
        group_name = group_map[instance.role]
        group, created = Group.objects.get_or_create(name=group_name)
        
        # Nettoyer les anciens groupes
        instance.user.groups.clear()
        # Ajouter au nouveau groupe
        instance.user.groups.add(group)