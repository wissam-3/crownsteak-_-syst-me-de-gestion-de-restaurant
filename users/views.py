from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            
            # Redirection selon le groupe de l'utilisateur
            if user.groups.filter(name='serveur').exists():
                return redirect('serveur_dashboard')
            elif user.groups.filter(name='chef').exists():
                return redirect('chef_dashboard')
            elif user.groups.filter(name='caissier').exists():
                return redirect('caissier_dashboard')
            else:
                # Client normal
                return redirect('accueil')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
            return render(request, 'users/login.html', {'error': 'Identifiants invalides'})
    
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('accueil')