from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import OrdemPagamento, RegiaoFranqueado
from servicos.models import SolicitacaoServico
from django.contrib import messages

@login_required
def gerar_pagamento(request, solicitacao_id):
    solicitacao = get_object_or_404(SolicitacaoServico, id=solicitacao_id)
    if not hasattr(solicitacao, 'ordem_pagamento'):
        ordem = OrdemPagamento.objects.create(
            solicitacao=solicitacao,
            valor_total=solicitacao.valor,
        )
        ordem.dividir_valores()
        messages.success(request, "Ordem de pagamento gerada com sucesso!")
    else:
        messages.warning(request, "Ordem de pagamento já existe.")
    return redirect('pagamentos:lista_pagamentos')

@login_required
def lista_pagamentos(request):
    pagamentos = OrdemPagamento.objects.filter(status='pendente')
    return render(request, 'pagamentos/lista_pagamentos.html', {'pagamentos': pagamentos})

@login_required
def marcar_como_pago(request, pagamento_id):
    pagamento = get_object_or_404(OrdemPagamento, id=pagamento_id)
    pagamento.status = 'pago'
    pagamento.save()
    messages.success(request, "Pagamento marcado como pago!")
    return redirect('pagamentos:lista_pagamentos')