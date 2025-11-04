# /financeiro/urls.py (CORRIGIDO E COMPLETO)

from django.urls import path
from . import views

urlpatterns = [
    # --- Vistas de Página ---
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('historico/', views.historico, name='historico'),
    
    # --- Vistas de API ---
    path('api/dados-grafico/', views.dados_grafico, name='dados_grafico'),
    
    # API para o novo formulário AJAX (que usa FormData)
    path('api/cadastrar-movimentacao/', views.cadastrar_movimentacao_api, name='cadastrar_movimentacao_api'),
]