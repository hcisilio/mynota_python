# -*- coding: utf-8 -*-
from datetime import datetime
from django import forms
from django.contrib.admin import widgets
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from mynota.models import *


class LoginForm(forms.Form):
	usuario = forms.CharField(
		label = '',
		max_length = 30,
		widget=forms.TextInput(attrs={'placeholder': 'Nome de usuário', 'class': 'form-control edits'})
	)

	senha = forms.CharField(
		label = '',
		max_length = 30,
		widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'class': 'form-control edits'})
	)

	def clean_usuario(self):
		usuario = self.cleaned_data.get('usuario')
		if not User.objects.filter(username=usuario):
			raise forms.ValidationError(u'Usuário informado não existe.')
		return usuario

	def clean_senha(self):
		usuario = self.cleaned_data.get('usuario')
		senha = self.cleaned_data.get('senha')
		if not authenticate(username=usuario, password=senha):
			raise forms.ValidationError(u'Senha incorreta.')
		return senha

	def logar(self):
		usuario = self.cleaned_data.get('usuario')
		senha = self.cleaned_data.get('senha')
		return authenticate(username=usuario, password=senha)

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        exclude = ['user',]

        widgets={
            "matricula": forms.TextInput(attrs={'class':'edits', 'size':'20'}),
            "nome":forms.TextInput(attrs={'class':'edits', 'size':'30'}),
            "sobrenome":forms.TextInput(attrs={'class':'edits', 'size':'60'}),
            "email":forms.TextInput(attrs={'class':'edits', 'size':'60'}),
            #"turma": autocomplete.ModelSelect2Multiple(url='turma-autocomplete', attrs={'class': 'edits'}),
            "comentario":forms.Textarea(attrs={'class':'edits', 'rows':4, 'cols':70}),
        }
        labels = {
            'matricula': 'Matrícula',
            'email': 'e-mail',
            'turma': 'Turma',
        }
    class Media:
        css = {
            'all': ('/static/css/autocomplete.css',)
        }

    def clean_turma(self):
        turmas = self.cleaned_data.get('turma')
        for i in range(0, len(turmas)-1):
            for j in range(0, len(turmas)-1-i):
                if turmas[j].curso == turmas[j + 1].curso:
                    raise forms.ValidationError(u'Aluno não pode ser matriculado em turmas de mesmo curso (turmas %s e %s são do curso %s)' % (turmas[j].codigo, turmas[j+1].codigo, turmas[j].curso))
        return turmas

class AulaForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AulaForm, self).__init__(*args, **kwargs)
		self.fields['data'].initial = datetime.today().date()
	class Meta:
		model = Aula
		exclude = ['professor',]

		widgets = {
			"turma": forms.Select(attrs={'class':'edits'}),	
			"data": forms.DateInput(attrs={'class':'edits br-data-widget datepicker', 'size': '10'}),
			"conteudo": forms.Textarea(attrs={'class': 'edits', 'cols': '70', 'rows': '10'})
		}

class CursoForm(forms.ModelForm):
	class Meta:
		model = Curso
		fields = ['codigo', 'nome']
		widgets={
		  "codigo":forms.TextInput(attrs={'class':'edits'}),
		  "nome":forms.TextInput(attrs={'class':'edits', 'size':'50'}),
		}

class DiaForm(forms.ModelForm):
	class Meta:
		model = Dia
		fields = ['nome',]
		widgets={
		  "nome":forms.TextInput(attrs={'placeholder':'Nome','class':'form-control edits'}),
		}

class ModuloForm(forms.ModelForm):
	class Meta:
		model = Modulo
		fields = ['nome', 'curso']
		widgets={
		  "nome":forms.TextInput(attrs={'class':'edits', 'size':'50'}),
		  "curso":forms.Select(attrs={'class':'fedits', 'size':'50'})
		}

class PlanoAulaForm(forms.ModelForm):
	class Meta:
		model = PlanoAula
		exclude = ['professor',]

		widgets = {
			"turma": forms.Select(attrs={'class':'edits'}),
			"modulo": forms.Select(attrs={'class':'edits'}),
			"data": forms.DateInput(attrs={'class':'edits br-data-widget datepicker', 'size': '10'}),
			"conteudo": forms.Textarea(attrs={'class': 'edits', 'cols': '70', 'rows': '10'})
		}

class ProfessorForm(forms.ModelForm):
	method = 'POST'
	class Meta:
		model = Professor
		exclude = ['user',]
		widgets={
			"username":forms.TextInput(attrs={'class':'edits', 'size':'30'}),
			"nome":forms.TextInput(attrs={'class':'edits', 'size':'30'}),
			"sobrenome":forms.TextInput(attrs={'class':'edits', 'size':'60'}),
			"email":forms.TextInput(attrs={'class':'edits', 'size':'60'}),
			"disciplina_padrao":forms.Select(attrs={'class':'edits'}),
			"comentario":forms.Textarea(attrs={'class':'edits', 'rows':4, 'cols':70}),
		}
		labels = {
			'username': u'Nome de usuário',
			'email': u'E-mail',
			'comentario': u'Comentário',
			'disciplina_padrao': u'Disciplina Padrão'
		}

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['codigo', 'curso', 'professor', 'dia', 'situacao']
        widgets={
            "codigo":forms.TextInput(attrs={'class':'edits'}),
            "curso":forms.Select(attrs={'class':'edits'}),
            #"professor": autocomplete.ModelSelect2(url='professor-autocomplete', attrs={'class': 'edits'}),
            "situacao": forms.CheckboxInput(attrs={'class':'edits'}),
            "dia":forms.CheckboxSelectMultiple(),
        }
        labels = {
            'codigo': u'Código',
            'curso': u'Curso',
            'professor': 'Professor',
            'situacao': u'Turma Ativa?',
            'dia': 'Dias',
        }
    class Media:
        css = {
            'all': ('/static/css/autocomplete.css',)
        }
