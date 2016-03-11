# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from mynota.forms import *
from mynota.models import *

admin.site.disable_action('delete_selected')
# Register your models here.
class ProfessorInline(admin.StackedInline):
    model = Professor
    max_num = 1
    can_delete = False

class AlunoInline(admin.StackedInline):
    model = Aluno
    max_num = 1
    can_delete = False

class UserAdmin(AuthUserAdmin):
    inlines = [ProfessorInline, AlunoInline]

# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)

class ProfessorAdmin(admin.ModelAdmin):
    ordering = ('user__first_name',)
    search_fields = ('user__first_name',)
    list_display = ('id', 'get_nome', 'get_situacao', 'comentario', 'user')
    # list_filter = ('get_situacao',)
    list_display_icons = True
    export_to_xls = True
    form = ProfessorForm
admin.site.register(Professor, ProfessorAdmin)

class AlunoAdmin(admin.ModelAdmin):
    ordering = ('user__first_name',)
    search_fields = ('user__first_name', 'matricula')
    # list_display = ('matricula', 'user__first_name','user__email', 'link_to_detail')
    form = AlunoForm
admin.site.register(Aluno, AlunoAdmin)

class DiaAdmin(admin.ModelAdmin):
    search_fields = ('nome',)
admin.site.register(Dia, DiaAdmin)

class Modulo(admin.StackedInline):
    model = Modulo
    form = ModuloForm

class CursoAdmin(admin.ModelAdmin):
    ordering = ('nome',)
    search_fields = ('nome',)
    list_display = ('codigo', 'nome',)
    form = CursoForm
    inlines = [
        Modulo,
    ]
admin.site.register(Curso, CursoAdmin)

class TurmaAdmin(admin.ModelAdmin):
    ordering = ('codigo',)
    search_fields = ('codigo', 'professor', 'curso')
    list_display = ('codigo', 'professor', 'curso', 'get_dias', 'situacao', 'link_to_detail')
    list_filter = ('situacao',)
    form = TurmaForm

    def view_on_site(self, obj):
        return reverse('turma_detail', kwargs={'id': obj.id})    
admin.site.register(Turma, TurmaAdmin)

# class AulaAdmin(admin.ModelAdmin):
#     search_fields = ('turma', 'professor', 'data')
#     list_display = ('turma', 'professor', 'data', 'conteudo')
# admin.site.register(Aula, AulaAdmin)

class PlanoAulaAdmin(admin.ModelAdmin):
    search_fields = ('turma', 'professor', 'data', 'modulo')
admin.site.register(PlanoAula, PlanoAulaAdmin)
