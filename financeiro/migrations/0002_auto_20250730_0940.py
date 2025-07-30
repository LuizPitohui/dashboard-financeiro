#
# Copie e cole este código no seu novo arquivo de migração
# Ex: financeiro/migrations/0002_auto_... .py
#

from django.db import migrations
from django.contrib.auth import get_user_model

def create_superuser(apps, schema_editor):
    User = get_user_model()
    
    # !! MUDE ESTES VALORES PARA OS SEUS !!
    USERNAME = 'luiz.guedes'
    EMAIL = 'pitohuikun@gmail.com'
    PASSWORD = '159753@llT@'
    # !! ----------------------------- !!

    if not User.objects.filter(username=USERNAME).exists():
        print(f'Criando o superusuário {USERNAME}')
        User.objects.create_superuser(
            username=USERNAME,
            email=EMAIL,
            password=PASSWORD
        )
    else:
        print(f'O superusuário {USERNAME} já existe.')

class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0001_initial'), # Verifique se este é o nome da sua migração anterior
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]