# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import Group, User

class Pessoa(models.Model):
	user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
	nome = models.CharField(max_length=50, null=False, blank=False)
	sobrenome = models.CharField(max_length=256, null=False, blank=False)
	email = models.EmailField(null=True, blank=True)
	comentario = models.TextField(max_length=1000, null=True, blank=True)
	
	class Meta:
		abstract = True
	
	def nome_completo(self):
		return " ".join([self.user.first_name, self.user.last_name])
	nome_completo.short_description = u'Nome Completo'

	def get_situacao(self):
		return self.user.is_active
	get_situacao.short_description = u'Situação'

class Professor(Pessoa):
	username = models.CharField(max_length=20, unique=True)
	disciplina_padrao = models.CharField(max_length=50, choices=[[u'Administração', u'Administração'], [u'Informática', u'Informática'], [u'Inglês', 'Inglês']])

	class Meta:
		verbose_name = u'Professor'
		verbose_name_plural = u'Professores'

	def __unicode__(self):
		return u'%s %s'%(self.user.first_name, self.user.last_name)

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
		return ("<a href='/turma/detalhes/%s'> <span class='glyphicon glyphicon-search' aria-hidden='true'></span> </a><a href='/admin/mynota/turma/%s/change/'> <span class='glyphicon glyphicon-edit' aria-hidden='true'></span> </a>") % (self.id, self.id)
	link_to_detail.allow_tags = True
	link_to_detail.short_description = '#'

class Aluno(Pessoa):
	matricula = models.CharField(max_length=10, unique=True)
	turma = models.ManyToManyField(Turma)

	def __unicode__(self):
		return u'%s %s (%s)'%(self.nome, self.sobrenome, self.matricula)

	def link_to_detail(self):
		return ("<a href='/aluno/detalhes/%s'> <span class='glyphicon glyphicon-search' aria-hidden='true'></span> </a><a href='/admin/mynota/aluno/%s/change/'> <span class='glyphicon glyphicon-edit' aria-hidden='true'></span> </a>") % (self.id, self.id)
	link_to_detail.allow_tags = True
	link_to_detail.short_description = '#'


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

	class Meta:
		unique_together = ("aluno", "modulo")

	def __unicode__(self):
		return u'%s - %s'%(self.aluno, self.modulo)

	@classmethod
	def get_nota(self, aluno, modulo):
	    try:
	        return Nota.objects.get(aluno=aluno, modulo=modulo).valor
	    except Nota.DoesNotExist:
	        return 0.0


#Signals
from django.db.models.signals import pre_save
from django.dispatch import receiver
@receiver(pre_save, sender=Aluno)
@receiver(pre_save, sender=Professor)
def gerar_usuario(sender, instance, **kwargs):
	if not instance.id:
		if sender == Aluno:
			username = instance.matricula
		elif sender == Professor:
			username = instance.username
		novo_usuario = User(username=username, first_name=instance.nome, last_name=instance.sobrenome, email=instance.email)
		novo_usuario.set_password('123')
		novo_usuario.save()
		if sender == Aluno:
			novo_usuario.groups.add(Group.objects.get(name='Aluno'))
		elif sender == Professor:
			novo_usuario.is_staff=1
			novo_usuario.save()
			novo_usuario.groups.add(Group.objects.get(name='Professor'))
		instance.user = novo_usuario