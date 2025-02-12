from django.urls import path
from . import views

urlpatterns = [
    #path('servicos/', views.lista_servicos, name='lista_servicos'),
    path('solicitar/', views.criar_solicitacao, name='criar_solicitacao'),
    path('cadastro/cliente/', views.cadastro_cliente, name='cadastro_cliente'),
    path('painel/cliente', views.painel, name='painel_cliente'),
    path('minhas-solicitacoes/', views.minhas_solicitacoes, name='minhas_solicitacoes'),
    path('painel/', views.painel_cliente, name='painel_cliente'),
    path('aprovar/<int:solicitacao_id>/', views.aprovar_servico, name='aprovar_servico'),
    path('alterar-data/<int:solicitacao_id>/', views.alterar_data_solicitacao, name='alterar_data_solicitacao'),
    path('reclamacao/<int:solicitacao_id>/', views.registrar_reclamacao, name='registrar_reclamacao'),
    
    
]
