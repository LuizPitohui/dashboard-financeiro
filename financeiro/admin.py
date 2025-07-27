from django.contrib import admin
from .models import Movimentacao


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'valor', 'nome_pessoa', 'forma_pagamento', 'data_movimentacao', 'usuario']
    list_filter = ['tipo', 'forma_pagamento', 'data_movimentacao', 'usuario']
    search_fields = ['nome_pessoa', 'descricao']
    date_hierarchy = 'data_movimentacao'
    ordering = ['-data_criacao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'tipo', 'valor')
        }),
        ('Detalhes da Movimentação', {
            'fields': ('forma_pagamento', 'nome_pessoa', 'descricao')
        }),
        ('Datas', {
            'fields': ('data_movimentacao',)
        }),
    )

