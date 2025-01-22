from django.urls import path
from . import views

urlpatterns = [
    path('ordens/', views.listar_ordens, name='listar_ordens'),
    path('ordem/<int:ordem_id>/aceitar/', views.aceitar_ordem, name='aceitar_ordem'),
    path('ordem/<int:ordem_id>/finalizar/', views.finalizar_ordem, name='finalizar_ordem'),
]