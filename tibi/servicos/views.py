from django.shortcuts import render, redirect
from .models import Servico, SolicitacaoServico
from django.contrib.auth.decorators import login_required
from django.contrib import messages

"""
As views devem lidar com:
	1.	Listagem de serviços disponíveis.
	2.	Criação de solicitações.
	3.	Aprovação de orçamentos.
	4.	Reclamações.

Exemplo de View para criar solicitações:
"""


@login_required
def criar_solicitacao(request):
    if request.method == 'POST':
        servico_id = request.POST.get('servico')
        descricao = request.POST.get('descricao')
        data_solicitada = request.POST.get('data_solicitada')

        servico = Servico.objects.get(id=servico_id)
        solicitacao = SolicitacaoServico.objects.create(
            cliente=request.user,
            servico=servico,
            descricao=descricao,
            data_solicitada=data_solicitada,
            valor=servico.valor_base
        )
        messages.success(request, 'Solicitação criada com sucesso!')
        return redirect('minhas_solicitacoes')

    servicos = Servico.objects.all()
    return render(request, 'servicos/criar_solicitacao.html', {'servicos': servicos})

