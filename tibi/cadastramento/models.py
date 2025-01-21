from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Estados brasileiros
ESTADOS_CHOICES = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
]

class Email(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_emails')
    address = models.CharField(max_length=150)

    def __str__(self):
        if self.address:
            return f"email de {self.user.username}"
        return f"email sem usuario"

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"

class Servico(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_services')
    nome = models.CharField(max_length=60)
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        if self.nome:
            return f"colaborador {self.user.username}"  
        return f"colaborador sem serviço cadastrado"  

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        
class Cpf(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_cpf')
    numero = models.CharField(max_length=11)

    def __str__(self):
        if self.numero:
            return f"cpf de {self.user.username}"
        return f"cpf sem usuario"

    class Meta:
        verbose_name = "CPF"
        verbose_name_plural = "CPFs"

class Cnpj(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_cnpj')
    numero = models.CharField(max_length=14, null=True, blank=True)

    def __str__(self):
        if self.numero:
            return f"cnpj de {self.user.username}"

    class Meta:
        verbose_name = "CNPJ"
        verbose_name_plural = "CNPJs"

class Endereco(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_enderecos')
    cidade = models.CharField(max_length=35)
    estado = models.CharField(max_length=2, choices=ESTADOS_CHOICES)
    bairro = models.CharField(max_length=80)
    rua = models.CharField(max_length=80)
    num = models.CharField(max_length=7)

    def __str__(self):
        if self.cidade:
            return f"endereco de {self.user.username}"

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

class Prestador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='colaborador')
    nome = models.CharField(max_length=200)
    email = models.ManyToManyField(Email)
    idade = models.IntegerField()
    telefone = models.CharField(max_length=20)
    cpf = models.OneToOneField(Cpf, on_delete=models.CASCADE)
    cnpj = models.OneToOneField(Cnpj, on_delete=models.CASCADE, null=True, blank=True)
    razao_social = models.CharField(max_length=80, null=True, blank=True)
    ie = models.CharField(max_length=50, null=True, blank=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    servico = models.ManyToManyField(Servico)
    
    def __str__(self):
        if self.nome:
            return f"colaborador: {self.nome}"

    class Meta:
        verbose_name = "Prestador"
        verbose_name_plural = "Prestadores"

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente')
    nome = models.CharField(max_length=200)
    cpf = models.OneToOneField(Cpf, on_delete=models.CASCADE)
    endereco = models.ManyToManyField(Endereco)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20)
    idade = models.IntegerField()

    def __str__(self):
        if self.nome:
            return f"cliente: {self.nome}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

class Franqueado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='franqueado')
    nome = models.CharField(max_length=200)
    endereco = models.ManyToManyField(Endereco)
    clientes = models.ManyToManyField(Cliente)
    prestador = models.ManyToManyField(Prestador)

    def __str__(self):
        if self.nome:
            return f"franqueado {self.nome}"

    class Meta:
        verbose_name = "Franqueado"
        verbose_name_plural = "Franqueados"
