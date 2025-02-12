from django import forms
from cadastramento.models import Endereco, Cliente

class ClienteForm(forms.ModelForm):
    cpf = forms.CharField(max_length=11, required=True, label="CPF / CNPJ")
    telefone = forms.CharField(max_length=20, label="Telefone WhatsApp")
    email = forms.CharField(max_length=20, label="email")

    class Meta:
        model = Cliente
        fields = [
            'nome', 'endereco', 'cpf', 'telefone', 'email'
        ]
    class Meta:
        model = Endereco
        fields = [
            'cidade', 'estado', 'bairro', 'rua', 'num'
        ]

# servicos/forms.py
from django import forms
from .models import Reclamação

class ReclamaçãoForm(forms.ModelForm):
    class Meta:
        model = Reclamação
        fields = ['descricao', 'foto']
