from django.db import models
from django.contrib.auth.models import User
from servicos.models import SolicitacaoServico  # Importando do app de serviços

class OrdemPagamento(models.Model):
    solicitacao = models.OneToOneField(SolicitacaoServico, on_delete=models.CASCADE, related_name="ordem_pagamento")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    valor_prestador = models.DecimalField(max_digits=10, decimal_places=2)
    valor_franqueado = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('pago', 'Pago'),
        ],
        default='pendente'
    )

    def dividir_valores(self):
        percentual_prestador = 0.7  # 70% do valor total para o prestador
        percentual_franqueado = 0.3  # 30% do valor total para o franqueado
        self.valor_prestador = self.valor_total * percentual_prestador
        self.valor_franqueado = self.valor_total * percentual_franqueado
        self.save()

    def __str__(self):
        return f"Ordem #{self.id} - {self.status}"

class RegiaoFranqueado(models.Model):
    franqueado = models.ForeignKey(User, on_delete=models.CASCADE, related_name="regioes")
    regiao = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.regiao} - {self.franqueado.username}"
    

    