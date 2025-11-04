# /financeiro/management/commands/seed_data.py (CORRIGIDO)

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from financeiro.models import Movimentacao
from faker import Faker
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Preenche o banco de dados com dados mockados usando a biblioteca Faker.'

    def add_arguments(self, parser):
        parser.add_argument('--numero',
                            type=int,
                            default=500,
                            help='O número de movimentações a serem criadas (padrão: 50)')

    def handle(self, *args, **options):
        self.stdout.write("Iniciando o processo de mock de dados com Faker...")
        
        num_movimentacoes = options['numero']
        fake = Faker('pt_BR')  # Inicializa o Faker em Português do Brasil

        # --- 1. Encontrar o usuário 'admin' ---
        try:
            # Altere 'admin' se o seu superusuário tiver outro nome
            user = User.objects.get(username='admin')
            self.stdout.write(f"Usuário '{user.username}' encontrado.")
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(
                "Usuário 'admin' não encontrado. "
                "Por favor, crie um superusuário com: python manage.py createsuperuser"
            ))
            return

        # --- 2. Limpar dados antigos ---
        # <-- MUDANÇA AQUI (de user=user para usuario=user)
        Movimentacao.objects.filter(usuario=user).delete()
        self.stdout.write("Movimentações antigas deste usuário foram limpas.")

        # --- 3. Listas de dados fixos ---
        formas_pagamento = ['dinheiro', 'pix', 'cartao_credito', 'cartao_debito', 'boleto', 'transferencia']

        # --- 4. Criar novas movimentações ---
        self.stdout.write(f"Criando {num_movimentacoes} novas movimentações...")
        
        for _ in range(num_movimentacoes):
            tipo_mov = random.choice(['entrada', 'saida'])
            
            # Gera uma data/hora aleatória no último ano
            data_aleatoria = fake.date_time_between(start_date='-1y', end_date='now', 
                                                    tzinfo=timezone.get_current_timezone())
            
            if tipo_mov == 'entrada':
                nome = fake.name()
                desc = f"Pagamento {fake.bs()}"
                valor = round(random.uniform(200.0, 3000.0), 2)
            else: # Saída
                nome = fake.company()
                desc = fake.catch_phrase()
                valor = round(random.uniform(20.0, 800.0), 2)

            Movimentacao.objects.create(
                usuario=user, # <-- MUDANÇA AQUI (de user=user para usuario=user)
                tipo=tipo_mov,
                valor=valor,
                nome_pessoa=nome,
                descricao=desc,
                forma_pagamento=random.choice(formas_pagamento),
                data_movimentacao=data_aleatoria
                # Nota: o campo data_criacao é 'default=timezone.now', então não precisamos mexer
            )

        self.stdout.write(self.style.SUCCESS(
            # <-- MUDANÇA AQUI (para a mensagem ficar correta)
            f"\nSucesso! {num_movimentacoes} movimentações criadas para o usuário '{user.username}'."
        ))