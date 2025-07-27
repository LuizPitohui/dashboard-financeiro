from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastrar-movimentacao/', views.cadastrar_movimentacao, name='cadastrar_movimentacao'),
    path('historico/', views.historico, name='historico'),
    path('api/dados-grafico/', views.dados_grafico, name='dados_grafico'),
]

