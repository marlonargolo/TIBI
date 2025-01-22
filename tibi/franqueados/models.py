from django.db import models
from django.contrib.auth.models import User
from prestadores.models import OrdemServico, Recado
from servicos.models import SolicitacaoServico

class SolicitacaoOrcamento(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitacoes_orcamento')
    descricao = models.TextField()
    data_solicitada = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('aprovado', 'Aprovado'),
            ('recusado', 'Recusado'),
        ],
        default='pendente',
    )
    valor_estimado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Orçamento #{self.id} - {self.cliente.username}"


class OrdemServicoFranqueado(models.Model):
    ordem_servico = models.OneToOneField(OrdemServico, on_delete=models.CASCADE, related_name='franqueado_ordem')
    data_geracao = models.DateTimeField(auto_now_add=True)
    franqueado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordens_geradas')
    motivo_negacao = models.TextField(null=True, blank=True)
    foto_justificativa = models.ImageField(upload_to='ordens_negadas/', null=True, blank=True)

    def __str__(self):
        return f"Ordem #{self.ordem_servico.id} - Franqueado {self.franqueado.username}"


class AlertaReclamacao(models.Model):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='alertas')
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    resolvido = models.BooleanField(default=False)

    def __str__(self):
        return f"Alerta #{self.id} - Ordem {self.ordem_servico.id}"


class CadastroPrestador(models.Model):
    prestador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cadastros_pendentes')
    aprovado = models.BooleanField(default=False)
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Aprovado" if self.aprovado else "Pendente"
        return f"Prestador: {self.prestador.username} - {status}"