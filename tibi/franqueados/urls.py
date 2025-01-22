from django.urls import path
from . import views

app_name = 'franqueados'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('aprovar-prestador/<int:prestador_id>/', views.aprovar_prestador, name='aprovar_prestador'),
    path('gerar-ordem/<int:orcamento_id>/', views.gerar_ordem_servico, name='gerar_ordem'),
    path('resolver-reclamacao/<int:reclamacao_id>/', views.resolver_reclamacao, name='resolver_reclamacao'),
    path('grafico-ordens/', views.grafico_ordens, name='grafico_ordens'),
]