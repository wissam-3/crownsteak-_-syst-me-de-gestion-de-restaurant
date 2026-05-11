from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('detail/<int:plat_id>/', views.detail_plat, name='detail_plat'),
    path('panier/', views.panier, name='panier'),
]