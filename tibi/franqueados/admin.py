from django.contrib import admin
from .models import SolicitacaoOrcamento, OrdemServicoFranqueado, AlertaReclamacao, CadastroPrestador

@admin.register(SolicitacaoOrcamento)
class SolicitacaoOrcamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'status', 'valor_estimado', 'data_solicitada')
    list_filter = ('status', 'data_solicitada')
    search_fields = ('cliente__username', 'descricao')
    ordering = ('-data_solicitada',)


@admin.register(OrdemServicoFranqueado)
class OrdemServicoFranqueadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'ordem_servico', 'franqueado', 'data_geracao')
    search_fields = ('ordem_servico__descricao', 'franqueado__username')
    ordering = ('-data_geracao',)


@admin.register(AlertaReclamacao)
class AlertaReclamacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'ordem_servico', 'resolvido', 'data_criacao')
    list_filter = ('resolvido',)
    search_fields = ('ordem_servico__descricao',)
    ordering = ('-data_criacao',)


@admin.register(CadastroPrestador)
class CadastroPrestadorAdmin(admin.ModelAdmin):
    list_display = ('id', 'prestador', 'aprovado', 'data_solicitacao')
    list_filter = ('aprovado',)
    search_fields = ('prestador__username',)
    ordering = ('-data_solicitacao',)