from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Prestador, Cliente, Email
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from cadastramento.models import Prestador, Cpf, Cnpj, Endereco, Servico


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Prestador, Cpf, Cnpj, Endereco, Servico, Email
# views.py
from django.shortcuts import render, redirect
from .models import UserProfile

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile  # Supondo que UserProfile seja o modelo de perfil
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:  # Quando o usuário é criado, cria o perfil
        profile = UserProfile.objects.create(user=instance)
        # Defina o tipo de usuário automaticamente ou de acordo com alguma lógica
        profile.user_type = 'cliente'  # Defina um tipo padrão, como 'cliente'
        profile.save()

def cadastro_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')

        # Criar o usuário
        user = User.objects.create_user(username=email, email=email)
        user.save()

        # Criar o perfil do usuário
        profile = UserProfile(user=user, user_type=user_type)
        profile.save()

        # Redirecionar para a página apropriada
        if user_type == 'prestador':
            return redirect('cadastro_prestador')  # Redireciona para a página de cadastro de prestador
        elif user_type == 'cliente':
            return redirect('cadastro_cliente')  # Redireciona para a página de cadastro de cliente
        else:
            return redirect('tela_inicial')  # Página para usuários com ambos os perfis

    return render(request, 'cadastro_usuario.html')

@login_required
def redirecionar_usuario(request):
    profile = request.user.profile  # Obter o perfil do usuário

    if profile.user_type == 'cliente':
        return redirect('dashboard_cliente')  # Redireciona para o dashboard do cliente
    elif profile.user_type == 'prestador':
        return redirect('dashboard_prestador')  # Redireciona para o dashboard do prestador
    elif profile.user_type == 'ambos':
        return redirect('dashboard_ambos')  # Redireciona para o dashboard para ambos


def dashboard_cliente(request):
    return render(request, 'cliente/dashboard.html')

def dashboard_prestador(request):
    return render(request, 'prestador/dashboard.html')

def dashboard_ambos(request):
    return render(request, 'ambos/dashboard.html')


@login_required
def cadastro_prestador(request):
    if request.method == "POST":
        usuario = request.user

        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        idade = request.POST.get('idade', '0')
        cpf_cnpj = request.POST.get('cpf_cnpj')
        razao_social = request.POST.get('razao_social', '')
        ie = request.POST.get('ie', '')

        estado = request.POST.get('estado')
        cidade = request.POST.get('cidade')
        bairro = request.POST.get('bairro')
        rua = request.POST.get('rua')
        num = request.POST.get('num')

        area_servico = request.POST.getlist('area_servico')

        try:
            idade = int(idade) if idade.isdigit() else 0
        except ValueError:
            idade = 0

        cpf = None
        cnpj = None

        if len(cpf_cnpj) == 11:
            cpf, created = Cpf.objects.get_or_create(numero=cpf_cnpj, user=usuario)
        elif len(cpf_cnpj) == 14:
            cnpj, created = Cnpj.objects.get_or_create(numero=cpf_cnpj, user=usuario)
        else:
            return render(request, 'cadastro_prestador.html', {'erro': 'CPF ou CNPJ inválido'})

        # Impede salvar Prestador sem CPF ou CNPJ válido
        if not cpf and not cnpj:
            return render(request, 'cadastro_prestador.html', {'erro': 'Erro ao processar CPF/CNPJ'})

        endereco, created = Endereco.objects.get_or_create(
            user=usuario,
            defaults={'estado': estado, 'cidade': cidade, 'bairro': bairro, 'rua': rua, 'num': num}
        )
        if not created:
            endereco.estado = estado
            endereco.cidade = cidade
            endereco.bairro = bairro
            endereco.rua = rua
            endereco.num = num
            endereco.save()

        # Criando o prestador com CPF ou CNPJ garantido
        prestador = Prestador.objects.create(
            user=usuario,
            nome=nome,
            telefone=telefone,
            idade=idade,
            razao_social=razao_social,
            ie=ie,
            endereco=endereco,
            cpf=cpf,
            cnpj=cnpj
        )

        email_obj, created = Email.objects.get_or_create(address=email, user=usuario)
        prestador.email.add(email_obj)

        prestador.servico.clear()
        for servico_nome in area_servico:
            try:
                servico = Servico.objects.get(nome=servico_nome)
                prestador.servico.add(servico)
            except Servico.DoesNotExist:
                pass

        return redirect('sucesso')

    return render(request, 'cadastro_prestador.html')




def cadastro_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')
        bairro = request.POST.get('bairro')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        complemento = request.POST.get('complemento', '')
        cpf_cnpj = request.POST.get('cpf_cnpj')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')

        if User.objects.filter(username=email).exists():
            messages.error(request, "E-mail já cadastrado!")
            return redirect('cadastro_cliente')

        user = User.objects.create_user(username=email, email=email, first_name=nome)
        cliente = Cliente.objects.create(user=user)

        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect('tela_inicial')

    return render(request, 'cadastro_cliente.html')




def tela_inicial(request):
    return render(request, 'tela_inicial.html')


#redirecionar usuarios


@login_required
def redirecionar_usuario(request):
    if hasattr(request.user, 'profile'):
        if request.user.profile.user_type == 'cliente':
            return redirect('dashboard_cliente')
        elif request.user.profile.user_type == 'prestador':
            return redirect('dashboard_prestador')
        elif request.user.profile.user_type == 'franqueado':
            return redirect('dashboard_franqueado')
    return redirect('default_homepage')

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def home(request):
    # Tenta obter o perfil ou o cria se não existir
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'user_type': 'cliente'}  # Define um tipo padrão, se necessário
    )
    
    if user_profile.user_type == 'cliente':
        return redirect('cliente:cliente_dashboard')  # Redireciona para o dashboard do cliente
    elif user_profile.user_type == 'prestador':
        return redirect('prestador:prestador_dashboard')  # Redireciona para o dashboard do prestador
    else:
        return redirect('cadastro:escolher_tipo')  # Página para escolher o tipo de cadastro


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def escolher_tipo(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type not in ['cliente', 'prestador']:
            # Caso não seja um tipo válido
            return render(request, 'cadastro/escolher_tipo.html', {'error': 'Tipo inválido!'})
        
        # Atribuindo o tipo ao perfil
        user_profile = request.user.profile
        user_profile.user_type = user_type
        user_profile.save()
        
        # Redireciona para o dashboard com base no tipo
        if user_type == 'cliente':
            return redirect('cliente:cliente_dashboard')
        else:
            return redirect('prestador:prestador_dashboard')
    return render(request, 'escolher_tipo.html')

