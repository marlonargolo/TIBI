from django.urls import path
from . import views

urlpatterns = [
    #path('servicos/', views.lista_servicos, name='lista_servicos'),
    path('solicitar/', views.criar_solicitacao, name='criar_solicitacao'),
    #path('minhas-solicitacoes/', views.minhas_solicitacoes, name='minhas_solicitacoes'),
]
