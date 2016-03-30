# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core import serializers
import json
from mynota.models import *
from mynota.forms import *
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/entrar/')

def entrar(request):
    next=request.GET.get('next', '/home/')
    if request.method == 'POST':
        next = request.POST.get('next', '/home/')
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.logar()
            login(request, usuario)
            return HttpResponseRedirect(next)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'next': next} )

def sair(request):
    logout(request)
    return HttpResponseRedirect('/')

def home(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin/')
    return render(request, 'home.html', )

def aluno_detail(request, id):
    aluno = get_object_or_404(Aluno, pk=id)
    turmas = Turma.objects.filter(aluno = aluno)
    # notas = Nota.objects.filter(aluno=aluno)
    return render(request, 'aluno_detail.html', {'turmas': turmas, 'aluno': aluno}) 

def aula_add(request):
    if request.method == 'POST':
        form = AulaForm(request.POST)
        if form.is_valid():
            aula = Aula(
                professor = Professor.objects.get(user=request.user),
                turma = form.cleaned_data['turma'],
                data = form.cleaned_data['data'],
                conteudo = form.cleaned_data['conteudo']
            )
            aula.save()
            messages.success(request, 'Aula registrada com sucesso!')
            return HttpResponseRedirect('/aula/add/')
        else:
            messages.error(request, 'Preencha corretamente os campos indicados!')
    else:
        form = AulaForm()
    return render(request, 'aula_add.html', {'form': form})

def aula_delete(request, id):
    aula = get_object_or_404(Aula, pk=id, professor__user = request.user)
    aula.delete()
    messages.success(request, 'Aula removida com sucesso')
    return HttpResponseRedirect('/aula_add/')


def aulas_por_turma(request, turma):
    queryset = Aula.objects.filter(turma__pk=turma).order_by('data')
    list = [] #create list
    for row in queryset: #populate list
        if row.professor.user == request.user:
            list.append({'turma':row.turma.codigo, 'professor': row.professor.user.first_name +" "+ row.professor.user.last_name,'data': row.data.strftime('%d/%m/%Y'), 'conteudo': row.conteudo, 'id': row.id})
        else:
            list.append({'turma':row.turma.codigo, 'professor': row.professor.user.first_name +" "+ row.professor.user.last_name,'data': row.data.strftime('%d/%m/%Y'), 'conteudo': row.conteudo, 'id': False})
    recipe_list_json = json.dumps(list) #dump list as JSON
    return HttpResponse(recipe_list_json, 'application/javascript')

def modulos_por_turma(request, turma):
    turma = Turma.objects.get(pk=turma)
    queryset = Modulo.objects.filter(curso=turma.curso)
    list = [] #create list
    for row in queryset: #populate list
        list.append({'id':row.id, 'nome':row.nome})
    recipe_list_json = json.dumps(list) #dump list as JSON
    return HttpResponse(recipe_list_json, 'application/javascript')

def plano_aula_add(request):
    if request.method == 'POST':
        form = PlanoAulaForm(request.POST)
        if form.is_valid():
            # data_lista = request.POST['data'].split('/')
            # data = datetime(int(data_lista[2]),int(data_lista[1]),int(data_lista[0]))
            plano_aula = PlanoAula(
                turma = form.cleaned_data['turma'],
                modulo = form.cleaned_data['modulo'],
                professor = Professor.objects.get(user=request.user),
                data = form.cleaned_data['data'],
                conteudo = form.cleaned_data['conteudo'],
            )
            plano_aula.save()
            messages.success(request, 'Plano de aula registrado com sucesso')
            return HttpResponseRedirect('/plano_aula/add/')
    else:
        form = PlanoAulaForm()
    return render(request, 'plano_aula_add.html', {'form': form})

def planos_por_turma(request, turma):
    queryset = PlanoAula.objects.filter(turma__pk=turma).order_by('data')
    list = [] #create list
    for row in queryset: #populate list
        list.append({'turma':row.turma.codigo, 'modulo':row.modulo.nome, 'professor': row.professor.user.first_name +" "+ row.professor.user.last_name,'data': row.data.strftime('%d/%m/%Y'), 'conteudo': row.conteudo, 'id': row.id})
    recipe_list_json = json.dumps(list) #dump list as JSON
    return HttpResponse(recipe_list_json, 'application/javascript')

def turma_detail(request, id):
    turma = get_object_or_404(Turma, pk=id)
    return render(request, 'turma_detail.html', {'turma': turma,}) 

def filtro_turmas(request, opcao):
    if opcao == "minhas":
        queryset = Turma.objects.filter(professor__user=request.user, situacao=True)
    elif opcao == "todas":
        queryset = Turma.objects.filter(situacao=True)
    list = [] #create list
    for row in queryset: #populate list
        list.append({'pk': row.pk, 'codigo':row.codigo, 'curso': row.curso.nome})
    recipe_list_json = json.dumps(list) #dump list as JSON
    return HttpResponse(recipe_list_json, 'application/javascript')

def listar_notas(request):
    if request.method == 'POST':
        form = PlanoAulaForm(request.POST)
        if form.is_valid():
            # data_lista = request.POST['data'].split('/')
            # data = datetime(int(data_lista[2]),int(data_lista[1]),int(data_lista[0]))
            plano_aula = PlanoAula(
                turma = form.cleaned_data['turma'],
                modulo = form.cleaned_data['modulo'],
                professor = Professor.objects.get(user=request.user),
                data = form.cleaned_data['data'],
                conteudo = form.cleaned_data['conteudo'],
            )
            plano_aula.save()
            messages.success(request, 'Plano de aula registrado com sucesso')
            return HttpResponseRedirect('/plano_aula/add/')
    else:
        form = PlanoAulaForm()
    return render(request, 'nota_add.html', {'form': form})

def notas_da_turma(request, turma):
    turma = get_object_or_404(Turma, pk=turma)
    queryset = turma.aluno_set.all()
    list = [] #create list
    for row in queryset: #populate list
        notas = []
        for modulo in turma.curso.modulo.all():
            nota = [modulo.id, Nota.get_nota(aluno=row, modulo=modulo)]
            notas.append(nota)
        list.append({'aluno':[row.id, row.nome_completo()], 'notas': notas})
    recipe_list_json = json.dumps(list) #dump list as JSON
    return HttpResponse(recipe_list_json, 'application/javascript')

# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
def lancar_nota(request):
    if request.method == "POST" and request.is_ajax():
        aluno = get_object_or_404(Aluno, pk=request.POST['aluno_id'])
        modulo = get_object_or_404(Modulo, pk=request.POST['modulo_id'])
        try:
            nota = Nota.objects.get(aluno=aluno, modulo=modulo)
            nota.valor = float(request.POST['valor'])
            nota.save()
        except Nota.DoesNotExist:
            Nota.objects.create(aluno=aluno, modulo=modulo, valor=float(request.POST['valor']))
        
        response_data = {'result': 'Nota lançada!'}
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )