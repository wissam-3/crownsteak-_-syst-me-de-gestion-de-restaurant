from django.urls import path
from . import views

urlpatterns = [
    path('valider/', views.valider_commande, name='valider_commande'),
    path('suivi/<int:commande_id>/', views.suivi_commande, name='suivi_commande'),
    path('suivi/', views.suivi_commande_session, name='suivi_commande'),  # Sans ID, utilise la session
    path('chef/', views.chef_dashboard, name='chef_dashboard'),
    path('serveur/', views.serveur_dashboard, name='serveur_dashboard'),
    path('caissier/', views.caissier_dashboard, name='caissier_dashboard'),
]