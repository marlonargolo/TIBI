from django.contrib import admin
from .models import OrdemPagamento, RegiaoFranqueado

@admin.register(OrdemPagamento)
class OrdemPagamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'solicitacao', 'valor_total', 'status', 'data_pagamento')
    list_filter = ('status', 'data_pagamento')
    search_fields = ('solicitacao__cliente__username',)

@admin.register(RegiaoFranqueado)
class RegiaoFranqueadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'franqueado', 'regiao')
    search_fields = ('franqueado__username', 'regiao')