from django.db import models
from django.contrib.auth.models import User

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    valor_base = models.DecimalField(max_digits=10, decimal_places=2)  # Valor padrão do serviço
    prazo_execucao = models.IntegerField(help_text="Prazo em dias")  # Tempo médio de execução

    def __str__(self):
        return self.nome


class SolicitacaoServico(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitacoes')
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    descricao = models.TextField()
    data_solicitada = models.DateField()
    profissional = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicos_realizados')
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('agendado', 'Agendado'),
            ('finalizado', 'Finalizado'),
            ('cancelado', 'Cancelado'),
 ],
        default='pendente'
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Pode ser atualizado após orçamento
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observacoes = models.TextField(null=True, blank=True)

    def calcular_valor_final(self):
        return self.valor - self.desconto

    def __str__(self):
        return f"Solicitação #{self.id} - {self.servico.nome} por {self.cliente.username}"


class Reclamação(models.Model):
    solicitacao = models.ForeignKey(SolicitacaoServico, on_delete=models.CASCADE, related_name='reclamacoes')
    descricao = models.TextField()
    foto = models.ImageField(upload_to='reclamacoes/', null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reclamação da Solicitação #{self.solicitacao.id}"


#modelos para fornecedores:

class Fornecedor(models.Model):
    nome = models.CharField(max_length=150)
    contato = models.CharField(max_length=100)
    email = models.EmailField()
    produtos = models.TextField()  # Lista de produtos fornecidos

    def __str__(self):
        return self.nome
