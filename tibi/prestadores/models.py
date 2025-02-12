from django.db import models
from django.contrib.auth.models import User
from django.db import models
from cadastramento.models import Prestador  # Importando o modelo Prestador do app cadastro

class OrdemServico(models.Model):
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordens_cliente')
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE, related_name='ordens_prestador')  # Alteração para usar o modelo Prestador
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_solicitada = models.DateField()
    data_realizacao = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('aceita', 'Aceita'),
            ('negada', 'Negada'),
            ('finalizada', 'Finalizada'),
        ],
        default='pendente'
    )
    foto_cliente = models.ImageField(upload_to='ordens/fotos_clientes/', null=True, blank=True)
    justificativa = models.TextField(null=True, blank=True)
    reclamacao = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Ordem #{self.id} - {self.cliente.username} -> {self.prestador.nome}"


class Agenda(models.Model):
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE, related_name='agenda')  # Alteração para usar o modelo Prestador
    ordem = models.OneToOneField(OrdemServico, on_delete=models.CASCADE)
    data = models.DateField()
    alerta_1dia = models.BooleanField(default=False)

    def __str__(self):
        return f"Agenda de {self.prestador.nome} - Ordem #{self.ordem.id}"


class Recado(models.Model):
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE, related_name='recados')  # Alteração para usar o modelo Prestador
    ordem = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    descricao = models.TextField()
    foto_anexo = models.ImageField(upload_to='recados/', null=True, blank=True)
    data_envio = models.DateTimeField(auto_now_add=True)
    lido = models.BooleanField(default=False)

    def __str__(self):
        return f"Recado para {self.prestador.nome} - Ordem #{self.ordem.id}"


class Relatorio(models.Model):
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE, related_name='relatorios')  # Alteração para usar o modelo Prestador
    total_ordens = models.IntegerField(default=0)
    total_valor = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    data_geracao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Relatório {self.data_geracao} - {self.prestador.nome}"
    

# Model Notificacao
class Notificacao(models.Model):
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE)  # Alteração para usar o modelo Prestador
    mensagem = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificação para {self.prestador.nome}: {self.mensagem}"
