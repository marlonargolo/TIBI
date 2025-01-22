from django.contrib import admin
from .models import OrdemServico, Agenda, Recado, Relatorio

@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'prestador', 'status', 'data_solicitada', 'data_realizacao', 'valor')
    list_filter = ('status', 'data_realizacao', 'prestador')
    search_fields = ('cliente__username', 'prestador__username', 'descricao')
    ordering = ('-data_solicitada',)

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'prestador', 'ordem', 'data', 'alerta_1dia')
    list_filter = ('data', 'prestador')
    search_fields = ('prestador__username', 'ordem__descricao')
    ordering = ('-data',)

@admin.register(Recado)
class RecadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'prestador', 'ordem', 'data_envio', 'lido')
    list_filter = ('data_envio', 'lido')
    search_fields = ('ordem__descricao', 'prestador__username')
    ordering = ('-data_envio',)

@admin.register(Relatorio)
class RelatorioAdmin(admin.ModelAdmin):
    list_display = ('id', 'prestador', 'total_ordens', 'total_valor', 'data_geracao')
    list_filter = ('data_geracao',)
    search_fields = ('prestador__username',)
    ordering = ('-data_geracao',)


from django.http import JsonResponse
from .models import OrdemServico

def grafico_ordens(request):
    ordens = OrdemServico.objects.filter(prestador=request.user, status='finalizada')
    data = {
        'labels': [ordem.data_realizacao.strftime('%d/%m/%Y') for ordem in ordens],
        'values': [float(ordem.valor) for ordem in ordens],
    }
    return JsonResponse(data)