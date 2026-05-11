from django.urls import path
from . import views

urlpatterns = [
    path('demande/<int:commande_id>/', views.demande_facture, name='demande_facture'),
    path('facture/<int:commande_id>/', views.facture, name='facture'),
    path('caissier/', views.caissier_dashboard, name='caissier_dashboard'),
    path('caissier/paiement/<int:commande_id>/', views.paiement_caissier, name='paiement_caissier'),
]