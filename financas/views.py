from django.shortcuts import render, redirect
from .models import Movimento, Perfil
from django.http import HttpResponse
import csv


def acesso(request, pessoa):
    perfil = Perfil.objects.get(pessoa=pessoa)

    if perfil.senha:
        if request.method == 'POST':
            if request.POST.get('senha') == perfil.senha:
                request.session['pessoa'] = pessoa
                return redirect('dashboard')
            return render(request, 'financas/senha.html', {'erro': True})

        return render(request, 'financas/senha.html', {'pessoa': pessoa})

    request.session['pessoa'] = pessoa
    return redirect('dashboard')

def escolher_pessoa(request, pessoa):
    if pessoa not in ['IAN', 'JULIA', 'JUNTOS']:
        return redirect('/')

    request.session['pessoa'] = pessoa
    return redirect('dashboard')



def dashboard(request):
    pessoa = request.session.get('pessoa')
    if not pessoa:
        return render(request, 'financas/acesso.html')

    movimentos = Movimento.objects.all().order_by('-data')

    total_entradas = sum(m.valor for m in movimentos if m.tipo == 'entrada')
    total_saidas = sum(m.valor for m in movimentos if m.tipo == 'saida')
    saldo = total_entradas - total_saidas

    return render(request, 'financas/dashboard.html', {
        'movimentos': movimentos,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo': saldo,
        'pessoa': pessoa
    })


def adicionar(request):
    pessoa = request.session.get('pessoa')
    if not pessoa:
        return redirect('dashboard')

    if request.method == 'POST':
        Movimento.objects.create(
            tipo=request.POST['tipo'],
            pessoa=pessoa,
            origem=request.POST['origem'],
            valor=request.POST['valor'],
        )
        return redirect('dashboard')

    return render(request, 'financas/adicionar.html', {'pessoa': pessoa})


def exportar_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="financas.csv"'

    writer = csv.writer(response)
    writer.writerow(['Tipo', 'Pessoa', 'Origem', 'Valor', 'Data'])

    for m in Movimento.objects.all():
        writer.writerow([m.tipo, m.pessoa, m.origem, m.valor, m.data])

    return response

def sair(request):
    request.session.flush()
    return redirect('/')

def lista_detalhada(request):
    pessoa = request.session.get('pessoa')
    if not pessoa:
        return redirect('/')

    movimentos = Movimento.objects.all().order_by('origem')

    return render(request, 'financas/lista_detalhada.html', {
        'movimentos': movimentos,
        'pessoa': pessoa
    })
