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