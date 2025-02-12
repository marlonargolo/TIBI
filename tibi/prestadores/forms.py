from django import forms
from cadastramento.models import Prestador, Cpf, Cnpj, Endereco, Servico

class PrestadorForm(forms.ModelForm):
    cpf = forms.CharField(max_length=11, required=False, label="CPF")
    cnpj = forms.CharField(max_length=14, required=False, label="CNPJ")
    razao_social = forms.CharField(max_length=80, required=False, label="Razão Social")
    ie = forms.CharField(max_length=50, required=False, label="IE")
    
    servico = forms.ModelMultipleChoiceField(
        queryset=Servico.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Área de Serviço"
    )

    class Meta:
        model = Prestador
        fields = [
            'nome', 'email', 'telefone', 'cpf', 'cnpj', 'razao_social', 'ie', 'endereco', 'servico'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['endereco'].queryset = Endereco.objects.all()
