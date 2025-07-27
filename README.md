# Sistema de Controle Financeiro UNI

Sistema completo de controle financeiro desenvolvido em Django com interface moderna e responsiva.

## ✨ Funcionalidades

- **Autenticação**: Sistema de login/logout seguro
- **Dashboard**: Visão geral com gráficos e estatísticas
- **Cadastro de Movimentações**: Modais para entrada e saída de dinheiro
- **Histórico**: Tabela completa com filtros avançados
- **Tema Claro/Escuro**: Alternância entre temas
- **Responsivo**: Interface adaptável para desktop e mobile

## 🚀 Instalação e Execução

### 1. Clonar o projeto
```bash
cd controle_financeiro
```

### 2. Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Executar migrações
```bash
python manage.py migrate
```

### 5. Criar superusuário (opcional)
```bash
python manage.py createsuperuser
```

### 6. Executar servidor
```bash
python manage.py runserver
```

Acesse: http://localhost:8000

## 👤 Usuário de Teste

- **Usuário**: manus
- **Senha**: manus_password_123

## 📱 Funcionalidades Detalhadas

### Dashboard
- Cards com totais de entradas, saídas e saldo
- Gráfico de movimentação financeira
- Filtros por período (semanal, mensal, anual)
- Últimas movimentações

### Cadastro de Movimentações
- Modal para entrada de dinheiro
- Modal para saída de dinheiro
- Campos: forma de pagamento, valor, nome da pessoa, descrição
- Validação em tempo real

### Histórico
- Tabela com todas as movimentações
- Filtros por nome, tipo e período
- Design limpo e profissional
- Paginação automática

### Interface
- Navbar com logo UNI e informações do usuário
- Sidebar com navegação principal
- Tema claro/escuro com persistência
- Design responsivo com Bootstrap 5

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.2.4
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5.3.0
- **Ícones**: Bootstrap Icons
- **Gráficos**: Chart.js
- **Banco de Dados**: SQLite (desenvolvimento)

## 📂 Estrutura do Projeto

```
controle_financeiro/
├── controle_financeiro/     # Configurações do Django
├── financeiro/              # App principal
│   ├── models.py           # Modelo Movimentacao
│   ├── views.py            # Views do sistema
│   └── urls.py             # URLs do app
├── templates/               # Templates HTML
│   ├── base.html           # Template base
│   ├── registration/       # Templates de autenticação
│   └── financeiro/         # Templates do app
├── static/                  # Arquivos estáticos
│   ├── css/                # Estilos CSS
│   └── js/                 # Scripts JavaScript
├── requirements.txt         # Dependências
└── manage.py               # Script de gerenciamento
```

## 🎨 Personalização

### Cores do Tema
- **Primária**: #0d6efd (azul)
- **Sucesso**: #198754 (verde)
- **Perigo**: #dc3545 (vermelho)
- **Tema Escuro**: #212529 (cinza escuro)

### Modificar Estilos
Edite o arquivo `static/css/style.css` para personalizar:
- Cores do tema
- Animações
- Layout responsivo
- Estilos dos componentes

## 📊 Modelo de Dados

### Movimentacao
- `usuario`: ForeignKey para User
- `tipo`: CharField (entrada/saida)
- `valor`: DecimalField
- `forma_pagamento`: CharField
- `nome_pessoa`: CharField
- `descricao`: TextField
- `data_criacao`: DateTimeField
- `data_movimentacao`: DateField

## 🔧 Configurações

### Settings Importantes
- `LANGUAGE_CODE = 'pt-br'`
- `TIME_ZONE = 'America/Sao_Paulo'`
- `LOGIN_URL = '/login/'`
- `CSRF_TRUSTED_ORIGINS` configurado

## 📈 Próximas Melhorias

- [ ] Relatórios em PDF
- [ ] Exportação para Excel
- [ ] Categorias de movimentação
- [ ] Metas financeiras
- [ ] Notificações
- [ ] API REST

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

---

**Desenvolvido com ❤️ para controle financeiro eficiente**

