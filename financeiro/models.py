from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Movimentacao(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    
    FORMA_PAGAMENTO_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('pix', 'PIX'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('boleto', 'Boleto'),
        ('transferencia', 'Transferência Bancária'),
        ('cheque', 'Cheque'),
        ('outros', 'Outros'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES)
    nome_pessoa = models.CharField(max_length=200, help_text="Nome da pessoa que está pagando ou recebendo")
    descricao = models.TextField(help_text="Motivo da entrada ou saída")
    data_criacao = models.DateTimeField(default=timezone.now)
    data_movimentacao = models.DateField(default=timezone.now)
    
    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Movimentação'
        verbose_name_plural = 'Movimentações'
    
    def __str__(self):
        return f"{self.get_tipo_display()} - R$ {self.valor} - {self.nome_pessoa}"
    
    @property
    def valor_formatado(self):
        return f"R$ {self.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

