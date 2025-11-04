/* static/js/script.js */

// Espera o DOM carregar para executar o script
document.addEventListener('DOMContentLoaded', function() {

    // --- 1. Lógica para abrir Modais ---
    // (Esta função é chamada pelo HTML)
    window.abrirModal = function(tipo) {
        var modalCadastro = bootstrap.Modal.getInstance(document.getElementById('modalCadastro'));
        if (modalCadastro) {
            modalCadastro.hide();
        }

        var modalAlvoId = (tipo === 'entrada') ? 'modalEntrada' : 'modalSaida';
        var modalAlvo = new bootstrap.Modal(document.getElementById(modalAlvoId));
        modalAlvo.show();
    }


    // --- 2. Função Reutilizável para mostrar "Toasts" (Notificações) ---
    const toastContainer = document.querySelector('.toast-container');
    
    function showToast(message, type = 'success') {
        const toastId = 'toast-' + Math.random().toString(36).substr(2, 9);
        const toastColorClass = (type === 'success') ? 'bg-custom-success' : 'bg-custom-danger';
        
        const toastHTML = `
            <div id="${toastId}" class="toast align-items-center text-white ${toastColorClass} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;

        toastContainer.insertAdjacentHTML('beforeend', toastHTML);
        
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
        toast.show();

        // Limpa o toast do DOM depois que ele se esconde
        toastElement.addEventListener('hidden.bs.toast', function () {
            toastElement.remove();
        });
    }


    // --- 3. Lógica para Submissão de Formulário via AJAX ---
    
    // Seleciona os formulários
    const formEntrada = document.getElementById('formEntrada');
    const formSaida = document.getElementById('formSaida');

    // Função genérica para lidar com a submissão
    async function handleFormSubmit(event, tipo) {
        event.preventDefault(); // Previne o recarregamento da página

        const form = event.target;
        const submitButton = form.querySelector('button[type="submit"]');
        const originalButtonHTML = submitButton.innerHTML;

        // Mostrar estado de "Loading" no botão
        submitButton.disabled = true;
        submitButton.innerHTML = `
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Salvando...
        `;

        // Coletar dados do formulário
        const formData = new FormData(form);
        formData.append('tipo', tipo); // Adiciona o tipo ('entrada' ou 'saida')

        try {
            const response = await fetch('/api/cadastrar-movimentacao/', {
                method: 'POST',
                body: formData,
                headers: {
                    // O CSRF Token é pego do <input> dentro do formulário
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                    'X-Requested-With': 'XMLHttpRequest' // Informa ao Django que é um AJAX
                }
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                // Sucesso!
                const modalInstance = bootstrap.Modal.getInstance(form.closest('.modal'));
                modalInstance.hide(); // Fecha o modal
                form.reset(); // Limpa os campos do formulário
                
                showToast(data.message || 'Movimentação salva!', 'success');
                
                // Recarrega a página para atualizar o dashboard
                setTimeout(() => {
                    location.reload();
                }, 1500); // Espera 1.5s para o usuário ler o toast

            } else {
                // Erro vindo do servidor (ex: validação)
                showToast(data.message || 'Erro ao salvar. Verifique os dados.', 'danger');
            }

        } catch (error) {
            // Erro de rede ou JavaScript
            console.error('Erro no fetch:', error);
            showToast('Erro de conexão. Tente novamente.', 'danger');
        } finally {
            // Restaura o botão em qualquer caso
            submitButton.disabled = false;
            submitButton.innerHTML = originalButtonHTML;
        }
    }

    // Adiciona os "listeners" aos formulários
    if (formEntrada) {
        formEntrada.addEventListener('submit', (e) => handleFormSubmit(e, 'entrada'));
    }
    if (formSaida) {
        formSaida.addEventListener('submit', (e) => handleFormSubmit(e, 'saida'));
    }

});