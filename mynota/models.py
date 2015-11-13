# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Professor(models.Model):
	user = models.OneToOneField(User, null=False, blank=False)
	comentario = models.TextField(max_length=1000, null=True, blank=True)

	class Meta:
		verbose_name = u'Professor'
		verbose_name_plural = u'Professores'

	def __unicode__(self):
		return u'%s %s'%(self.user.first_name, self.user.last_name)

	def get_nome(self):
		return " ".join([self.user.first_name, self.user.last_name])
	get_nome.short_description = u'Nome Completo'

	def get_situacao(self):
		return self.user.is_active
	get_situacao.short_description = u'Situação'

	def save(self, *args, **kwargs):		
		try:
			usuario = User.objects.get(username=request.POST['login'])
		except User.DoesNotExist:
			usuario = User.objects.create_user(request.POST['login'], request.POST['email'], request.POST['senha'])
		self.user = usuario
		super(Professor, self).save(*args, **kwargs)

class Dia(models.Model):
	nome = models.CharField(max_length=15, unique=True)

	class Meta:
		ordering = ['id',]

	def __unicode__(self):
		return u'%s'%(self.nome)

class Curso(models.Model):
	codigo = models.CharField(max_length=20, unique=True, null=True)
	nome = models.CharField(max_length=45)

	def __unicode__(self):
		return u'%s'%(self.nome)

class Modulo(models.Model):
	nome = models.CharField(max_length=45)
	curso = models.ForeignKey(Curso, related_name='modulo')

	def __unicode__(self):
		return u'%s'%(self.nome)

class Turma(models.Model):
	codigo = models.CharField(u'Código', max_length=10, unique=True)
	professor = models.ForeignKey(Professor, related_name='turma')
	curso = models.ForeignKey(Curso, related_name='turma')
	situacao = models.BooleanField(u'Situação', default=True)
	dia = models.ManyToManyField(Dia)

	def __unicode__(self):
		return u'%s (%s)'%(self.codigo, self.curso)

	def get_dias(self):
		return "; ".join([d.nome for d in self.dia.all()])
	get_dias.short_description = 'Dias de Aula'

	def link_to_detail(self):		
		return ("<a href='/turma/detalhes/%s'> Detalhes </a>") % (self.id)
	link_to_detail.allow_tags = True
	link_to_detail.short_description = 'Detalhes'

class Aluno(models.Model):
	matricula = models.CharField(max_length=10, unique=True)
	nome = models.CharField(max_length=75)
	email = models.EmailField(max_length=100, null=True, blank=True)
	turma = models.ManyToManyField(Turma)

	def __unicode__(self):
		return u'%s - %s'%(self.matricula, self.nome)

	def link_to_detail(self):		
		return ("<a href='/aluno/detalhes/%s'> Detalhes </a>") % (self.id)
	link_to_detail.allow_tags = True
	link_to_detail.short_description = 'Detalhes'

class Aula(models.Model):
	turma = models.ForeignKey(Turma, related_name='aula')
	professor = models.ForeignKey(Professor, related_name='aula')
	data = models.DateField()
	conteudo = models.TextField(max_length=2048)

	def __unicode__(self):
		return u'%s - %s'%(self.id, self.turma.codigo)

class PlanoAula(models.Model):
	turma = models.ForeignKey(Turma, related_name='plano_aula')
	modulo = models.ForeignKey(Modulo, related_name='plano_aula')
	professor = models.ForeignKey(Professor, related_name='plano_aula')
	data = models.DateField()
	conteudo = models.TextField(max_length=2048)

	class Meta:
		verbose_name = u'Plano de aula'
		verbose_name_plural = u'Planos de aula'

	def __unicode__(self):
		return u'%s - %s (%s)'%(self.id, self.turma.codigo, self.modulo.nome)

class Nota(models.Model):
	aluno = models.ForeignKey(Aluno, related_name='nota')
	modulo = models.ForeignKey(Modulo, related_name='nota')
	valor = models.FloatField()

	def __unicode__(self):
		return u'%s - %s'%(self.aluno, self.modulo)
