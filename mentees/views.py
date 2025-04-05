from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Navigators, Mentorados

def mentorados(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.constants.ERROR, "Você não está logado para acessar a página anterior!")
        return redirect('/usuarios/login')
    
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
