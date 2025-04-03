from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not password == confirm_password:
            messages.add_message(request, constants.ERROR, "As senhas devem ser iguais!")
            return redirect(cadastro)
        
        if not len(password) >= 6:
            messages.add_message(request, constants.ERROR, "A senha deve conter pelo menos 6 caracteres")
            return redirect(cadastro)
        
        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request, constants.ERROR, f"O usuário {username} já existe!")
            return redirect(cadastro)
        
        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('/usuarios/login')

