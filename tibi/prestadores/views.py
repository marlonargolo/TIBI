from django.shortcuts import render, get_object_or_404, redirect
from .models import OrdemServico, Recado, Agenda
from django.contrib.auth.decorators import login_required

def listar_ordens(request):
    if hasattr(request.user, 'prestador'):
        # Assuming that 'prestador' is a related field linking User to Prestador model
        ordens = OrdemServico.objects.filter(prestador=request.user.prestador).order_by('-data_solicitada')
    else:
        ordens = []
    
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


#cadastro de prestador

from django.shortcuts import render, redirect
from .forms import PrestadorForm
from cadastramento.models import Cpf, Cnpj

def cadastro_prestador(request):
    if request.method == "POST":
        form = PrestadorForm(request.POST)
        if form.is_valid():
            prestador = form.save(commit=False)
            
            # Criando CPF e CNPJ se forem informados
            if form.cleaned_data.get('cpf'):
                cpf = Cpf.objects.create(numero=form.cleaned_data['cpf'], user=prestador.user)
                prestador.cpf = cpf
            
            if form.cleaned_data.get('cnpj'):
                cnpj = Cnpj.objects.create(numero=form.cleaned_data['cnpj'], user=prestador.user)
                prestador.cnpj = cnpj

            prestador.save()
            form.save_m2m()  # Para salvar os serviços escolhidos
            return redirect('sucesso')  # Redireciona para uma página de sucesso

    else:
        form = PrestadorForm()

    return render(request, 'prestadores/cadastro_prestador.html', {'form': form})


# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import OrdemServico, Agenda, Notificacao
from servicos.models import Servico, Reclamação
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from cadastramento.models import Prestador

@login_required
def dashboard(request):
    try:
        prestador = request.user.colaborador  # Acessando o prestador do usuário
    except Prestador.DoesNotExist:
        # Caso o usuário não tenha um prestador associado
        return redirect('prestadores:cadastro_prestador')  # Redirecionar para a página de cadastro de prestador

    # Carregar os serviços disponíveis, ordens de serviço e reclamações do prestador
    servicos = Servico.objects.all()
    ordens = OrdemServico.objects.filter(prestador=prestador, status='pendente')
    reclamacoes = Reclamação.objects.filter(prestador=prestador)
    notificacoes = Notificacao.objects.filter(prestador=prestador)

    return render(request, 'prestadores/dashboard.html', {
        'servicos': servicos,
        'ordens': ordens,
        'reclamacoes': reclamacoes,
        'notificacoes': notificacoes
    })


@login_required
def aceitar_ordem(request, ordem_id):
    ordem = get_object_or_404(OrdemServico, id=ordem_id, prestador=request.user.colaborador, status='pendente')  # Corrigido
    if ordem.data < timezone.now():
        return redirect('prestador:dashboard')

    # Verificar conflito de agenda
    conflitos = Agenda.objects.filter(prestador=request.user.colaborador, data=ordem.data)  # Corrigido
    if conflitos.exists():
        return render(request, 'prestador/erro_agenda.html', {'ordem': ordem})

    ordem.status = 'aceito'
    ordem.save()
    Agenda.objects.create(prestador=request.user.colaborador, ordem=ordem, data=ordem.data)

    return redirect('prestador:dashboard')

@login_required
def recusar_ordem(request, ordem_id):
    ordem = get_object_or_404(OrdemServico, id=ordem_id, prestador=request.user.prestador, status='pendente')
    ordem.status = 'recusado'
    ordem.save()

    # Redirecionar para a tela de ordens
    return redirect('prestador:dashboard')

@login_required
def reclamar_ordem(request, reclamacao_id):
    reclamacao = get_object_or_404(Reclamação, id=reclamacao_id, prestador=request.user.prestador)

    if request.method == 'POST':
        # Registrar a justificativa da reclamação
        reclamacao.justificativa = request.POST['justificativa']
        if 'foto' in request.FILES:
            reclamacao.foto = request.FILES['foto']
        reclamacao.save()

        # Enviar recado ao franqueado
        # Código para enviar mensagem ao franqueado (não detalhado)

        return redirect('prestador:dashboard')

    return render(request, 'prestador/reclamar_ordem.html', {'reclamacao': reclamacao})

@login_required
def add_agenda(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    
    if request.method == 'POST':
        data = request.POST['data']
        # Criar agendamento para o serviço escolhido
        Agenda.objects.create(prestador=request.user.prestador, servico=servico, data=data)
        
        # Notificar o prestador
        Notificacao.objects.create(prestador=request.user.prestador, mensagem=f"Serviço {servico.nome} agendado para {data}")

        return redirect('prestador:dashboard')

    return render(request, 'prestador/adicionar_agenda.html', {'servico': servico})

@login_required
def gerar_contrato(request, ordem_id):
    ordem = get_object_or_404(OrdemServico, id=ordem_id, prestador=request.user.prestador)

    if request.method == 'POST':
        # Gerar contrato (pode ser um documento PDF, por exemplo)
        # Código para gerar o contrato (não detalhado)
        
        return redirect('prestador:dashboard')

    return render(request, 'prestador/gerar_contrato.html', {'ordem': ordem})
