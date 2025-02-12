from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Cria o perfil do usuário
        profile = UserProfile.objects.create(user=instance)
        # Defina o tipo de usuário automaticamente
        if instance.email.endswith('@exemplo.com'):  # Apenas um exemplo
            profile.user_type = 'cliente'
        else:
            profile.user_type = 'prestador'
        profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


from django.db.models.signals import post_save
from django.dispatch import receiver
from servicos.models import Servico as ServicoServicos
from cadastramento.models import Servico as ServicoCadastramento

# Sincronizar quando um serviço for salvo no app "servicos"
@receiver(post_save, sender=ServicoServicos)
def sincronizar_servico_servicos(sender, instance, **kwargs):
    servico, created = ServicoCadastramento.objects.update_or_create(
        nome=instance.nome,
        defaults={
            'descricao': instance.descricao,
            'valor': instance.valor_base,
        }
    )

# Sincronizar quando um serviço for salvo no app "cadastramento"
@receiver(post_save, sender=ServicoCadastramento)
def sincronizar_servico_cadastramento(sender, instance, **kwargs):
    servico, created = ServicoServicos.objects.update_or_create(
        nome=instance.nome,
        defaults={
            'descricao': instance.descricao,
            'valor_base': instance.valor,
            'prazo_execucao': 0,  # Valor padrão, caso não seja informado
        }
    )
