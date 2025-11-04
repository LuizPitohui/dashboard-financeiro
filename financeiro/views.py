# /financeiro/views.py (CORRIGIDO E COMPLETO)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Movimentacao
import json
from decimal import Decimal, InvalidOperation # <-- Importações necessárias

# --- Vistas de Autenticação ---

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# --- Vistas de Página ---

@login_required
def dashboard(request):
    # Usamos request.user para que cada usuário veja apenas os seus dados
    entradas = Movimentacao.objects.filter(
        usuario=request.user, tipo='entrada'
    ).aggregate(total=Sum('valor'))['total'] or 0
    
    saidas = Movimentacao.objects.filter(
        usuario=request.user, tipo='saida'
    ).aggregate(total=Sum('valor'))['total'] or 0
    
    saldo_total = entradas - saidas
    
    ultimas_movimentacoes = Movimentacao.objects.filter(
        usuario=request.user
    ).order_by('-data_movimentacao')[:5]
    
    context = {
        'saldo_total': saldo_total,
        'total_entradas': entradas,
        'total_saidas': saidas,
        'ultimas_movimentacoes': ultimas_movimentacoes,
    }
    
    return render(request, 'financeiro/dashboard.html', context)


@login_required
def historico(request):
    movimentacoes = Movimentacao.objects.filter(usuario=request.user).order_by("-data_movimentacao")
    
    # Filtros
    nome_filtro = request.GET.get('nome', '')
    periodo_filtro = request.GET.get('periodo', '')
    tipo_filtro = request.GET.get('tipo', '')
    
    if nome_filtro:
        movimentacoes = movimentacoes.filter(nome_pessoa__icontains=nome_filtro)
    
    if tipo_filtro:
        movimentacoes = movimentacoes.filter(tipo=tipo_filtro)
    
    if periodo_filtro:
        hoje = timezone.now().date()
        if periodo_filtro == 'hoje':
            movimentacoes = movimentacoes.filter(data_movimentacao=hoje)
        elif periodo_filtro == 'semana':
            inicio_semana = hoje - timedelta(days=hoje.weekday())
            movimentacoes = movimentacoes.filter(data_movimentacao__gte=inicio_semana)
        elif periodo_filtro == 'mes':
            inicio_mes = hoje.replace(day=1)
            movimentacoes = movimentacoes.filter(data_movimentacao__gte=inicio_mes)
        elif periodo_filtro == 'ano':
            inicio_ano = hoje.replace(month=1, day=1)
            movimentacoes = movimentacoes.filter(data_movimentacao__gte=inicio_ano)
    
    # Calcular totais das movimentações filtradas
    total_entradas_historico = movimentacoes.filter(tipo='entrada').aggregate(Sum('valor'))['valor__sum'] or 0
    total_saidas_historico = movimentacoes.filter(tipo='saida').aggregate(Sum('valor'))['valor__sum'] or 0

    context = {
        'movimentacoes': movimentacoes,
        'nome_filtro': nome_filtro,
        'periodo_filtro': periodo_filtro,
        'tipo_filtro': tipo_filtro,
        'total_entradas_historico': total_entradas_historico,
        'total_saidas_historico': total_saidas_historico,
    }
    
    return render(request, 'financeiro/historico.html', context)


# --- Vistas de API ---

@login_required
def dados_grafico(request):
    periodo = request.GET.get('periodo', 'mensal')
    hoje = timezone.now().date()
    
    if periodo == 'semanal':
        inicio = hoje - timedelta(days=7)
    elif periodo == 'mensal':
        inicio = hoje - timedelta(days=30)
    elif periodo == 'anual':
        inicio = hoje - timedelta(days=365)
    else:
        inicio = hoje - timedelta(days=30)
    
    # Filtra por usuário logado
    movimentacoes = Movimentacao.objects.filter(
        usuario=request.user, data_movimentacao__gte=inicio
    )
    
    # Agrupar por data
    dados = {}
    for mov in movimentacoes:
        data_str = mov.data_movimentacao.strftime('%Y-%m-%d')
        if data_str not in dados:
            dados[data_str] = {'entradas': 0, 'saidas': 0}
        
        if mov.tipo == 'entrada':
            dados[data_str]['entradas'] += float(mov.valor)
        else:
            dados[data_str]['saidas'] += float(mov.valor)
    
    # Converter para formato do gráfico
    labels = sorted(dados.keys())
    entradas = [dados[data]['entradas'] for data in labels]
    saidas = [dados[data]['saidas'] for data in labels]
    
    return JsonResponse({
        'labels': labels,
        'entradas': entradas,
        'saidas': saidas
    })


@login_required
def cadastrar_movimentacao_api(request):
    """
    View de API para cadastrar uma movimentação via AJAX (Fetch).
    Esta view espera FormData, não JSON.
    """
    if request.method == 'POST':
        try:
            tipo = request.POST.get('tipo')
            valor = request.POST.get('valor')
            nome_pessoa = request.POST.get('nome_pessoa')
            descricao = request.POST.get('descricao')
            forma_pagamento = request.POST.get('forma_pagamento')

            # --- Validação ---
            if not all([tipo, valor, nome_pessoa, forma_pagamento]):
                return JsonResponse({'status': 'error', 'message': 'Todos os campos obrigatórios devem ser preenchidos.'}, status=400)
            
            if tipo not in ['entrada', 'saida']:
                return JsonResponse({'status': 'error', 'message': 'Tipo de movimentação inválido.'}, status=400)
            
            try:
                valor_decimal = Decimal(valor.replace(',', '.'))
                if valor_decimal <= 0:
                    raise InvalidOperation
            except InvalidOperation:
                 return JsonResponse({'status': 'error', 'message': 'O valor deve ser um número positivo.'}, status=400)

            # --- Criação do Objeto ---
            Movimentacao.objects.create(
                usuario=request.user,
                tipo=tipo,
                valor=valor_decimal,
                nome_pessoa=nome_pessoa,
                descricao=descricao or "",
                forma_pagamento=forma_pagamento
            )
            
            return JsonResponse({'status': 'success', 'message': 'Movimentação cadastrada com sucesso!'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ocorreu um erro interno: {str(e)}'}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)