from django.contrib import admin
from .models import Email, Servico, Cpf, Cnpj, Endereco, Prestador, Cliente, Franqueado


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address')
    search_fields = ('address', 'user__username')
    list_filter = ('user',)


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'descricao', 'valor', 'user')
    search_fields = ('nome', 'descricao', 'user__username')
    list_filter = ('user',)


@admin.register(Cpf)
class CpfAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'user')
    search_fields = ('numero', 'user__username')
    list_filter = ('user',)


@admin.register(Cnpj)
class CnpjAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'user')
    search_fields = ('numero', 'user__username')
    list_filter = ('user',)


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cidade', 'estado', 'bairro', 'rua', 'num', 'user')
    search_fields = ('cidade', 'estado', 'bairro', 'user__username')
    list_filter = ('estado', 'user')


@admin.register(Prestador)
class PrestadorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'idade', 'telefone', 'user')
    search_fields = ('nome', 'user__username', 'cpf__numero')
    list_filter = ('idade',)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'idade', 'telefone', 'user')
    search_fields = ('nome', 'user__username', 'cpf__numero')
    list_filter = ('idade',)


@admin.register(Franqueado)
class FranqueadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'user')
    search_fields = ('nome', 'user__username')
    list_filter = ('user',)
