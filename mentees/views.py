from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Navigators, Mentorados, ScheduleAvailability
from datetime import datetime, timedelta
from .auth import validate_token

def mentorados(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.constants.ERROR, "Você não está logado para acessar a página anterior!")
        return redirect('login')
    
    if request.method == 'GET':
        navigators = Navigators.objects.filter(user=request.user)
        mentorados = Mentorados.objects.filter(user=request.user)

        stage_flat = [i[1] for i in Mentorados.stages_choices]

        stage_qtd = []
        for stage, stage2 in Mentorados.stages_choices:
            stage_qtd.append(mentorados.filter(stage=stage).count()) 

        return render(request, 'mentorados.html', {'navigators':navigators, 'stages':Mentorados.stages_choices, 'mentorados':mentorados, 'stage_flat': stage_flat, 'stage_qtd': stage_qtd})    
    
    if request.method == 'POST':
        name = request.POST.get('name')
        photo = request.FILES.get('photo')
        stage = request.POST.get('stage')
        navigator = request.POST.get('navigator')

        try:
            mentorado = Mentorados(
                name=name,
                photo=photo,
                stage=stage,
                navigator=Navigators.objects.get(id=int(navigator)),
                user=request.user
            )

            mentorado.save()
        except:
            messages.add_message(request, messages.constants.ERROR, 'Não foi possível cadastrar o mentorado.')
            return redirect('mentorados')

        messages.add_message(request, messages.constants.SUCCESS, 'Mentorado cadastrado com sucesso.')
        return redirect('mentorados')
    
def reunioes(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.constants.ERROR, "Você não está logado para acessar a página anterior!")
        return redirect('login')
    
    if request.method == 'GET':
        return render(request, 'reunioes.html')
    
    if request.method == 'POST':
        date = request.POST.get('date')

        formated_date = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        
        mentor_shedules = ScheduleAvailability.objects.filter(mentor=request.user).filter(
            start_date__gte=(formated_date - timedelta(minutes=50)),
            start_date__lte=(formated_date + timedelta(minutes=50))
        )

        if mentor_shedules.exists():
            messages.add_message(request, messages.constants.ERROR, "Este horário já tem um agendamento")
            return redirect(reunioes)

        schedule = ScheduleAvailability(
            start_date = formated_date,
            mentor = request.user
        )

        schedule.save()

        return redirect(reunioes)
    
def auth(request):
    if request.method == 'GET':
        return render(request, 'auth_mentorados.html')
    
    if request.method == 'POST':
        token = request.POST.get('token')

        if not Mentorados.objects.filter(token=token).exists():
            messages.add_message(request, messages.constants.ERROR, 'Token Inválido!')
            return redirect('auth_mentorado')
        
        response = redirect('escolher_dia')
        response.set_cookie('auth_token', token, max_age=3600)

        return response
    
def escolher_dia(request):
    if not validate_token(request.COOKIES.get('auth_token')):
        messages.add_message(request, messages.constants.ERROR, 'Insira seu token!')
        return redirect('auth_mentorado')
    
    if request.method == 'GET':
        availability = ScheduleAvailability.objects.filter(
            start_date__gte=datetime.now(),
            scheduled=False,
            mentor=validate_token(request.COOKIES.get('auth_token')).user

        ).values_list('start_date', flat=True)
        print(availability)
        return render(request, 'escolher_dia.html', {'horarios':availability})


