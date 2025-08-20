#financeiro\views.py
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


@login_required
def dashboard(request):
    # --- Calcular saldo total (AGORA INCLUI TODAS AS MOVIMENTAÇÕES) ---
    # Removemos o filtro 'usuario=request.user' para que o saldo seja global
    entradas = Movimentacao.objects.filter(
        tipo='entrada'
    ).aggregate(total=Sum('valor'))['total'] or 0
    
    saidas = Movimentacao.objects.filter(
        tipo='saida'
    ).aggregate(total=Sum('valor'))[
        'total'
    ] or 0
    
    saldo_total = entradas - saidas
    
    # --- Últimas movimentações (AGORA INCLUI TODAS AS MOVIMENTAÇÕES) ---
    # Removemos o filtro 'usuario=request.user' para que as últimas movimentações sejam globais
    ultimas_movimentacoes = Movimentacao.objects.all().order_by(
        '-data_movimentacao'
    )[:5] # Ordena pela data da movimentação, as 5 mais recentes
    
    context = {
        'saldo_total': saldo_total,
        'total_entradas': entradas,
        'total_saidas': saidas,
        'ultimas_movimentacoes': ultimas_movimentacoes,
    }
    
    return render(request, 'financeiro/dashboard.html', context)


@login_required
def cadastrar_movimentacao(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            movimentacao = Movimentacao.objects.create(
                usuario=request.user,
                tipo=data['tipo'],
                valor=data['valor'],
                forma_pagamento=data['forma_pagamento'],
                nome_pessoa=data['nome_pessoa'],
                descricao=data['descricao'],
                data_movimentacao=data.get('data_movimentacao', timezone.now().date())
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Movimentação cadastrada com sucesso!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao cadastrar movimentação: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})


@login_required
def historico(request):
    #movimentacoes = Movimentacao.objects.filter(usuario=request.user)
    movimentacoes = Movimentacao.objects.all().order_by("-data_movimentacao")
    
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
    
    movimentacoes = Movimentacao.objects.filter(
        data_movimentacao__gte=inicio
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

