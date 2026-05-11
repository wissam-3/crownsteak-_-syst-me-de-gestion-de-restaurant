from django.urls import path
from . import views

urlpatterns = [
    path('choisir/', views.choisir_table, name='choisir_table'),
]