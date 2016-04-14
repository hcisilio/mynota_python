# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from mynota.forms import *
from mynota.models import *

admin.site.disable_action('delete_selected')

#Fitro de turmas para aluno admin
class TurmaFilter(SimpleListFilter):
    title = 'turma' # or use _('country') for translated title
    parameter_name = 'turma'
    def lookups(self, request, model_admin):
        turmas = set([turma for turma in Turma.objects.filter(situacao=True)])
        return [(turma.id, turma) for turma in turmas]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(turma__id__exact=self.value())
        else:
            return queryset

# Register your models here.
class ProfessorAdmin(admin.ModelAdmin):
    ordering = ('nome', 'sobrenome')
    search_fields = ('nome', 'sobrenome')
    list_display = ('id', 'nome_completo', 'get_situacao', 'email', 'disciplina_padrao', 'user')
    # list_filter = ('get_situacao',)
    list_display_icons = True
    export_to_xls = True
    form = ProfessorForm
admin.site.register(Professor, ProfessorAdmin)

class AlunoAdmin(admin.ModelAdmin):
    ordering = ('nome', 'sobrenome')
    search_fields = ('nome', 'sobrenome', 'matricula')
    list_display = ('link_to_detail', 'matricula', 'nome_completo', )
    list_filter = (TurmaFilter, 'turma__curso', 'turma__situacao')
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
    search_fields = ('codigo', 'professor__nome', 'professor__sobrenome', 'curso__nome')
    list_display = ('link_to_detail', 'codigo', 'professor', 'curso', 'get_dias', 'situacao')
    list_filter = ('situacao',)
    form = TurmaForm

    def get_queryset(self, request):
        qs = super(TurmaAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(professor__user=request.user)

    def view_on_site(self, obj):
        return reverse('turma_detail', kwargs={'id': obj.id})
admin.site.register(Turma, TurmaAdmin)

