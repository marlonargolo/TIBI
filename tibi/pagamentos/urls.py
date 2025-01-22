from django.urls import path
from . import views

app_name = 'pagamentos'

urlpatterns = [
    path('', views.lista_pagamentos, name='lista_pagamentos'),
    path('gerar/<int:solicitacao_id>/', views.gerar_pagamento, name='gerar_pagamento'),
    path('pagar/<int:pagamento_id>/', views.marcar_como_pago, name='marcar_como_pago'),
]