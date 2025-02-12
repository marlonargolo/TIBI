from django.shortcuts import render, redirect
from .models import Servico, SolicitacaoServico
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import SolicitacaoServico
from django.http import JsonResponse

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


#cadastro de cliente

from django.shortcuts import render, redirect
from cadastramento.models import Cpf
from .forms import ClienteForm, ReclamaçãoForm

def cadastro_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            
            cpf = Cpf.objects.create(numero=form.cleaned_data['cpf'], user=cliente.user)
            cliente.cpf = cpf

            cliente.save()
            return redirect('sucesso')

    else:
        form = ClienteForm()

    return render(request, 'servicos/cadastro_cliente.html', {'form': form})

def painel(request):
    return render(request, 'servicos/painel_cliente.html')

# servicos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Servico as ServicoDisponivel, SolicitacaoServico
from datetime import date

@login_required
def painel_cliente(request):
    # Exemplo: Buscar todos os serviços disponíveis (pode ser filtrado por categoria, etc.)
    servicos = ServicoDisponivel.objects.all()
    
    # Buscar as solicitações do usuário (ordens já criadas)
    solicitacoes = SolicitacaoServico.objects.filter(cliente=request.user).order_by('-id')
    
    # Exemplo de alerta: Se a data escolhida já passou ou se a solicitação não tem profissional atribuído,
    # pode ser disparado um aviso para o cliente escolher outra data.
    for solicitacao in solicitacoes:
        if solicitacao.data_solicitada < date.today() and not solicitacao.profissional:
            messages.warning(request, f"A solicitação #{solicitacao.id} está com a data vencida e sem profissional. Por favor, escolha uma nova data!")
    
    context = {
        'servicos': servicos,
        'solicitacoes': solicitacoes,
    }
    return render(request, 'servicos/painel_cliente.html', context)

# servicos/views.py
@login_required
def aprovar_servico(request, solicitacao_id):
    solicitacao = get_object_or_404(SolicitacaoServico, id=solicitacao_id, cliente=request.user)
    # Verifica se o serviço já foi realizado e se há necessidade de confirmação do cliente
    if solicitacao.status == 'finalizado':
        solicitacao.status = 'aprovado'  # ou outro status definido
        solicitacao.save()
        messages.success(request, 'Serviço aprovado com sucesso!')
    else:
        messages.error(request, 'O serviço ainda não foi finalizado.')
    return redirect('painel_cliente')

# servicos/views.py
@login_required
def registrar_reclamacao(request, solicitacao_id):
    solicitacao = get_object_or_404(SolicitacaoServico, id=solicitacao_id, cliente=request.user)
    if request.method == 'POST':
        form = ReclamaçãoForm(request.POST, request.FILES)
        if form.is_valid():
            reclamacao = form.save(commit=False)
            reclamacao.solicitacao = solicitacao
            reclamacao.save()
            messages.success(request, 'Reclamação registrada com sucesso!')
            return redirect('painel_cliente')
    else:
        form = ReclamaçãoForm()
    return render(request, 'servicos/registrar_reclamacao.html', {'form': form, 'solicitacao': solicitacao})


def alterar_data_solicitacao(request, solicitacao_id):
    solicitacao = get_object_or_404(SolicitacaoServico, id=solicitacao_id)
    
    if request.method == "POST":
        nova_data = request.POST.get("nova_data")
        if nova_data:
            solicitacao.data = nova_data
            solicitacao.save()
            messages.success(request, "Data alterada com sucesso!")
            return JsonResponse({"status": "success", "message": "Data alterada com sucesso!"})
        else:
            return JsonResponse({"status": "error", "message": "Data inválida!"})
    
    return JsonResponse({"status": "error", "message": "Método não permitido!"})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def minhas_solicitacoes(request):
    solicitacoes = SolicitacaoServico.objects.filter(cliente=request.user)
    return render(request, 'servicos/minhas_solicitacoes.html', {'solicitacoes': solicitacoes})
