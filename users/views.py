from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('mentorados')
    
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
        
        user = User.objects.filter(username__iexact=username)

        if user.exists():
            messages.add_message(request, constants.ERROR, f"O usuário {username} já existe!")
            return redirect(cadastro)
        
        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('login')

  
def login(request):
    if request.user.is_authenticated:
        return redirect('mentorados')
    
    if request.method == 'GET':
        return render(request, 'login.html')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # if not (User.objects.filter(username__iexact=username)).exists():
        #     messages.add_message(request, constants.ERROR, "Este usuário não existe!")
        #     return redirect(login)

        user = auth.authenticate(request, username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('mentorados')

        messages.add_message(request, constants.ERROR, "Este usuário não existe!")
        return redirect(login)
    
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(login)
    
    messages.add_message(request, constants.ERROR, "Você não fez login ainda!")
    return redirect(login)
    


