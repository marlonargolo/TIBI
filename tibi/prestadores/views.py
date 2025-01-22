from django.shortcuts import render, get_object_or_404, redirect
from .models import OrdemServico, Recado, Agenda
from django.contrib.auth.decorators import login_required

@login_required
def listar_ordens(request):
    ordens = OrdemServico.objects.filter(prestador=request.user).order_by('-data_solicitada')
    return render(request, 'prestadores/listar_ordens.html', {'ordens': ordens})

@login_required
def aceitar_ordem(request, ordem_id):
    ordem = get_object_or_404(OrdemServico, id=ordem_id, prestador=request.user)
    if request.method == 'POST':
        ordem.status = 'aceita'
        ordem.save()
        Agenda.objects.create(prestador=request.user, ordem=ordem, data=ordem.data_realizacao)
        return redirect('listar_ordens')
    return render(request, 'prestadores/aceitar_ordem.html', {'ordem': ordem})

@login_required
def finalizar_ordem(request, ordem_id):
    ordem = get_object_or_404(OrdemServico, id=ordem_id, prestador=request.user)
    if request.method == 'POST':
        ordem.status = 'finalizada'
        ordem.save()
        return redirect('listar_ordens')
    return render(request, 'prestadores/finalizar_ordem.html', {'ordem': ordem})