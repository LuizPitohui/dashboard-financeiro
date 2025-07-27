// Gerenciamento de tema
function toggleTheme() {
    const html = document.documentElement;
    const themeIcon = document.getElementById('theme-icon');
    const currentTheme = html.getAttribute('data-theme');
    
    if (currentTheme === 'dark') {
        html.setAttribute('data-theme', 'light');
        themeIcon.className = 'bi bi-moon-fill';
        localStorage.setItem('theme', 'light');
    } else {
        html.setAttribute('data-theme', 'dark');
        themeIcon.className = 'bi bi-sun-fill';
        localStorage.setItem('theme', 'dark');
    }
}

// Carregar tema salvo
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const html = document.documentElement;
    const themeIcon = document.getElementById('theme-icon');
    
    html.setAttribute('data-theme', savedTheme);
    
    if (savedTheme === 'dark') {
        themeIcon.className = 'bi bi-sun-fill';
    } else {
        themeIcon.className = 'bi bi-moon-fill';
    }
}

// Abrir modal de cadastro
function abrirModal(tipo) {
    // Fechar modal de seleção
    const modalCadastro = bootstrap.Modal.getInstance(document.getElementById('modalCadastro'));
    modalCadastro.hide();
    
    // Abrir modal específico
    setTimeout(() => {
        if (tipo === 'entrada') {
            const modalEntrada = new bootstrap.Modal(document.getElementById('modalEntrada'));
            modalEntrada.show();
        } else {
            const modalSaida = new bootstrap.Modal(document.getElementById('modalSaida'));
            modalSaida.show();
        }
    }, 300);
}

// Função para cadastrar movimentação
function cadastrarMovimentacao(tipo, formData) {
    const data = {
        tipo: tipo,
        valor: parseFloat(formData.get('valor')),
        forma_pagamento: formData.get('forma_pagamento'),
        nome_pessoa: formData.get('nome_pessoa'),
        descricao: formData.get('descricao')
    };
    
    fetch('/cadastrar-movimentacao/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('success', data.message);
            // Fechar modal
            const modalId = tipo === 'entrada' ? 'modalEntrada' : 'modalSaida';
            const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
            modal.hide();
            
            // Limpar formulário
            document.getElementById(`form${tipo.charAt(0).toUpperCase() + tipo.slice(1)}`).reset();
            
            // Recarregar página após 1 segundo
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showAlert('danger', data.message);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        showAlert('danger', 'Erro ao cadastrar movimentação. Tente novamente.');
    });
}

// Função para obter cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Função para mostrar alertas
function showAlert(type, message) {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Inserir no início do main
    const main = document.querySelector('main');
    main.insertBefore(alertContainer, main.firstChild);
    
    // Remover automaticamente após 5 segundos
    setTimeout(() => {
        if (alertContainer.parentNode) {
            alertContainer.remove();
        }
    }, 5000);
}

// Formatar valores monetários
function formatarMoeda(input) {
    let value = input.value.replace(/\D/g, '');
    value = (value / 100).toFixed(2);
    input.value = value;
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Carregar tema
    loadTheme();
    
    // Event listeners para formulários
    const formEntrada = document.getElementById('formEntrada');
    const formSaida = document.getElementById('formSaida');
    
    if (formEntrada) {
        formEntrada.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            cadastrarMovimentacao('entrada', formData);
        });
    }
    
    if (formSaida) {
        formSaida.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            cadastrarMovimentacao('saida', formData);
        });
    }
    
    // Formatação de campos de valor
    const camposValor = document.querySelectorAll('input[name="valor"]');
    camposValor.forEach(campo => {
        campo.addEventListener('input', function() {
            // Permitir apenas números e ponto decimal
            this.value = this.value.replace(/[^0-9.]/g, '');
            
            // Garantir apenas um ponto decimal
            const parts = this.value.split('.');
            if (parts.length > 2) {
                this.value = parts[0] + '.' + parts.slice(1).join('');
            }
        });
    });
    
    // Validação em tempo real
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (!this.value.trim()) {
                    this.classList.add('is-invalid');
                } else {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid') && this.value.trim()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            });
        });
    });
    
    // Sidebar toggle para mobile
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
        
        // Fechar sidebar ao clicar fora (mobile)
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                    sidebar.classList.remove('show');
                }
            }
        });
    }
    
    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide alerts
    const alerts = document.querySelectorAll('.alert:not(.alert-dismissible)');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.remove();
                }
            }, 300);
        }, 5000);
    });
});

// Função para confirmar ações
function confirmarAcao(mensagem, callback) {
    if (confirm(mensagem)) {
        callback();
    }
}

// Função para loading
function showLoading(element) {
    const originalContent = element.innerHTML;
    element.innerHTML = '<span class="loading"></span> Carregando...';
    element.disabled = true;
    
    return function hideLoading() {
        element.innerHTML = originalContent;
        element.disabled = false;
    };
}

// Função para copiar para área de transferência
function copiarParaAreaTransferencia(texto) {
    navigator.clipboard.writeText(texto).then(function() {
        showAlert('success', 'Texto copiado para a área de transferência!');
    }, function(err) {
        console.error('Erro ao copiar texto: ', err);
        showAlert('danger', 'Erro ao copiar texto.');
    });
}

// Função para exportar dados (placeholder)
function exportarDados(formato) {
    showAlert('info', `Exportação em ${formato} será implementada em breve.`);
}

// Função para imprimir relatório
function imprimirRelatorio() {
    window.print();
}

