# controle_financeiro/settings.py

import os
from pathlib import Path
import environ  # Pacote para gerenciar variáveis de ambiente
import dj_database_url # Pacote para configurar o banco de dados a partir de uma URL

# --- 1. Inicialização do Environ ---
# Isso permite ler variáveis de um arquivo .env (para desenvolvimento local)
# e do ambiente do servidor (para produção no Render).
env = environ.Env(
    # Define o tipo e o valor padrão para a variável DEBUG
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Para desenvolvimento local, crie um arquivo .env na raiz do projeto
# e coloque suas variáveis lá (SECRET_KEY, DATABASE_URL, etc.)
# O Render irá injetar essas variáveis diretamente no ambiente.
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# --- 2. Configurações de Segurança Lidas do Ambiente ---
# SECURITY WARNING: keep the secret key used in production secret!
# A chave secreta agora é lida da variável de ambiente 'SECRET_KEY'.
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# O modo DEBUG será False em produção, a menos que a variável DEBUG=True seja definida.
DEBUG = env('DEBUG')

# Configure os hosts permitidos. Você DEVE adicionar a URL do seu site no Render aqui.
# Ex: 'dashboard-financeiro.onrender.com'
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Adicione a URL do seu site no Render para proteção CSRF.
# Ex: 'https://dashboard-financeiro.onrender.com'
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[] )


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'financeiro',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Posição correta
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'controle_financeiro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'controle_financeiro.wsgi.application'


# --- 3. Configuração do Banco de Dados para Supabase ---
# Esta é a mudança crucial. Ele tentará usar a DATABASE_URL do ambiente.
# Se não encontrar, usará um SQLite local (útil para testes iniciais).
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600, # Mantém as conexões vivas por 10 minutos
        conn_health_checks=True,
    )
}


# Password validation
# ... (sem alterações aqui)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
# ... (sem alterações aqui)
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Manaus'
USE_I18N = True
USE_TZ = True


# --- 4. Configuração de Arquivos Estáticos para WhiteNoise ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# Diretório para onde o `collectstatic` irá copiar os arquivos para o deploy.
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Armazenamento otimizado do WhiteNoise que comprime os arquivos.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login URLs
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'
