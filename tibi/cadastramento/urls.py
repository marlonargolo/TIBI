from django.urls import path
from .views import cadastro_prestador, cadastro_cliente, tela_inicial, home
from servicos.views import painel
from prestadores.views import dashboard

app_name = 'cliente'  # Defina o namespace para o app
app_name = 'prestadores'  # Defina o namespace para o app


urlpatterns = [
    path('', tela_inicial, name='tela_inicial'),
    path('cadastro/prestador/', cadastro_prestador, name='cadastro_prestador'),
    path('cadastro/cliente/', cadastro_cliente, name='cadastro_cliente'),
     # Outras URLs...
    path('redirecionar/', home, name='home'),

# URL do painel do cliente
    path('cliente/dashboard/', painel, name='cliente_dashboard'),

    # URL do painel do prestador
    path('prestador/dashboard/', dashboard, name='prestador_dashboard'),


]
