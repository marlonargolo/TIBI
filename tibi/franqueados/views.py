from django.http import JsonResponse
from .models import OrdemServicoFranqueado
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import SolicitacaoOrcamento, OrdemServicoFranqueado, AlertaReclamacao, CadastroPrestador
from django.contrib import messages

def grafico_ordens_franqueado(request):
    ordens = OrdemServicoFranqueado.objects.filter(franqueado=request.user)
    data = {
        'labels': [ordem.data_geracao.strftime('%d/%m/%Y') for ordem in ordens],
        'values': [ordem.ordem_servico.valor for ordem in ordens],
    }
    return JsonResponse(data)

# Página inicial do franqueado
@login_required
def dashboard(request):
    orcamentos = SolicitacaoOrcamento.objects.filter(status='pendente')
    reclamacoes = AlertaReclamacao.objects.filter(resolvido=False)
    prestadores_pendentes = CadastroPrestador.objects.filter(aprovado=False)
    return render(request, 'franqueados/dashboard.html', {
        'orcamentos': orcamentos,
        'reclamacoes': reclamacoes,
        'prestadores_pendentes': prestadores_pendentes,
    })

# Aprovação de prestadores
@login_required
def aprovar_prestador(request, prestador_id):
    prestador = get_object_or_404(CadastroPrestador, id=prestador_id)
    prestador.aprovado = True
    prestador.save()
    messages.success(request, f"Prestador {prestador.prestador.username} aprovado com sucesso.")
    return redirect('franqueados:dashboard')

# Gerar gráfico de ordens e valores
@login_required
def grafico_ordens(request):
    ordens = OrdemServicoFranqueado.objects.filter(franqueado=request.user)
    data = {
        'labels': [ordem.data_geracao.strftime('%d/%m/%Y') for ordem in ordens],
        'values': [ordem.ordem_servico.valor for ordem in ordens],
    }
    return JsonResponse(data)

# Gerar ordem de serviço
@login_required
def gerar_ordem_servico(request, orcamento_id):
    orcamento = get_object_or_404(SolicitacaoOrcamento, id=orcamento_id)
    OrdemServicoFranqueado.objects.create(
        ordem_servico=orcamento,
        franqueado=request.user,
    )
    orcamento.status = 'aprovado'
    orcamento.save()
    messages.success(request, "Ordem de serviço gerada com sucesso.")
    return redirect('franqueados:dashboard')

# Gerenciar reclamações
@login_required
def resolver_reclamacao(request, reclamacao_id):
    reclamacao = get_object_or_404(AlertaReclamacao, id=reclamacao_id)
    reclamacao.resolvido = True
    reclamacao.save()
    messages.success(request, "Reclamação resolvida com sucesso.")
    return redirect('franqueados:dashboard')


#parte 2

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import (
    SolicitacaoOrcamento, OrdemServicoFranqueado, AlertaReclamacao, CadastroPrestador
)
from prestadores.models import OrdemServico
from django.db.models import Count, Sum

@login_required
def lista_solicitacoes_orcamento(request):
    solicitacoes = SolicitacaoOrcamento.objects.order_by('-data_solicitada')
    return render(request, 'franqueados/lista_solicitacoes_orcamento.html', {'solicitacoes': solicitacoes})

@login_required
def gerar_ordem_servico(request, solicitacao_id):
    solicitacao = get_object_or_404(SolicitacaoOrcamento, id=solicitacao_id)

    if request.method == 'POST':
        ordem_servico = OrdemServico.objects.create(
            cliente=solicitacao.cliente,
            descricao=solicitacao.descricao
        )
        OrdemServicoFranqueado.objects.create(ordem_servico=ordem_servico, franqueado=request.user)
        
        solicitacao.status = 'aprovado'
        solicitacao.save()
        messages.success(request, "Ordem de serviço gerada com sucesso!")
        return redirect('lista_solicitacoes_orcamento')

    return render(request, 'franqueados/gerar_ordem_servico.html', {'solicitacao': solicitacao})

@login_required
def lista_alertas_reclamacoes(request):
    alertas = AlertaReclamacao.objects.order_by('-data_criacao')
    return render(request, 'franqueados/lista_alertas_reclamacoes.html', {'alertas': alertas})

@login_required
def aprovacao_prestadores(request):
    prestadores_pendentes = CadastroPrestador.objects.filter(aprovado=False)
    
    if request.method == 'POST':
        prestador_id = request.POST.get('prestador_id')
        prestador = get_object_or_404(CadastroPrestador, id=prestador_id)
        prestador.aprovado = True
        prestador.save()
        messages.success(request, "Prestador aprovado com sucesso!")
        return redirect('aprovacao_prestadores')

    return render(request, 'franqueados/aprovacao_prestadores.html', {'prestadores_pendentes': prestadores_pendentes})

@login_required
def dashboard_franqueado(request):
    total_ordens = OrdemServico.objects.count()
    ordens_negadas = OrdemServicoFranqueado.objects.exclude(motivo_negacao="").count()
    total_faturamento = SolicitacaoOrcamento.objects.filter(status='aprovado').aggregate(Sum('valor_estimado'))['valor_estimado__sum'] or 0

    return render(request, 'franqueados/dashboard.html', {
        'total_ordens': total_ordens,
        'ordens_negadas': ordens_negadas,
        'total_faturamento': total_faturamento
    })
