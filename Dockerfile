FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN pip install poetry

# Configura Poetry para não criar virtualenv dentro do container
RUN poetry config virtualenvs.create false

# Copia arquivos de dependência
COPY pyproject.toml poetry.lock ./

# Instala dependências
RUN poetry install --no-root --only main

# Copia o código
COPY . .

# Comando padrão
CMD ["gunicorn", "controle_financeiro.wsgi:application", "--bind", "0.0.0.0:8000"]
