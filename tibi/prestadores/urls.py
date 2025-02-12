from django.urls import path
from . import views

urlpatterns = [
    path('ordens/', views.listar_ordens, name='listar_ordens'),
    path('ordem/<int:ordem_id>/aceitar/', views.aceitar_ordem, name='aceitar_ordem'),
    path('ordem/<int:ordem_id>/finalizar/', views.finalizar_ordem, name='finalizar_ordem'),
    #path('cadastro/prestador', views.cadastro_prestador, name='cadastro_prestador'),


  # Painel do Prestador
    path('dashboard', views.dashboard, name='dashboard'),
    
    # Servicos e Agenda
    path('add_agenda/<int:servico_id>/', views.add_agenda, name='add_agenda'),
    
    # Ordens de Serviço
    path('ordens/', views.dashboard, name='ordens'),
    path('aceitar_ordem/<int:ordem_id>/', views.aceitar_ordem, name='aceitar_ordem'),
    path('recusar_ordem/<int:ordem_id>/', views.recusar_ordem, name='recusar_ordem'),
    #path('ver_ordem/<int:ordem_id>/', views.ver_ordem, name='ver_ordem'),
    
    # Reclamações
    path('reclamacoes/', views.dashboard, name='reclamacoes'),
    path('reclamar_ordem/<int:reclamacao_id>/', views.reclamar_ordem, name='reclamar_ordem'),
    
    # Gerar Contrato
    path('gerar_contrato/<int:ordem_id>/', views.gerar_contrato, name='gerar_contrato'),


  
]
