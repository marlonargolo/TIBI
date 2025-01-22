from django.contrib import admin
from .models import Servico, SolicitacaoServico, Reclamação

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'valor_base', 'prazo_execucao')
    search_fields = ('nome',)
    list_filter = ('prazo_execucao',)
    ordering = ('nome',)


@admin.register(SolicitacaoServico)
class SolicitacaoServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'servico', 'status', 'data_solicitada', 'profissional', 'valor', 'desconto')
    search_fields = ('cliente__username', 'servico__nome', 'status')
    list_filter = ('status', 'data_solicitada', 'profissional')
    ordering = ('-data_solicitada',)
    readonly_fields = ('calcular_valor_final',)
    fieldsets = (
        ("Informações do Cliente e Serviço", {
            'fields': ('cliente', 'servico', 'descricao')
        }),
        ("Detalhes da Solicitação", {
            'fields': ('data_solicitada', 'profissional', 'status', 'valor', 'desconto', 'calcular_valor_final', 'observacoes')
        }),
    )


@admin.register(Reclamação)
class ReclamaçãoAdmin(admin.ModelAdmin):
    list_display = ('id', 'solicitacao', 'data_criacao', 'descricao')
    search_fields = ('solicitacao__id', 'descricao')
    list_filter = ('data_criacao',)
    ordering = ('-data_criacao',)