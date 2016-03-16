from django.conf.urls import patterns, include, url
from django.contrib import admin
from mynota.autocomplete_light_registry import *
import mynota.views

admin.site.base_template = 'admin/mynota/base.html'
admin.site.base_site_template = 'admin/mynota/base_site.html'
admin.site.index_template = 'admin/mynota/index.html'
admin.site.login_template = 'admin/mynota/login.html'
admin.autodiscover()

urlpatterns = patterns('',
    #autocomplete
    url(
        'turma-autocomplete/$',
        AutocompleteTurma.as_view(),
        name='turma-autocomplete',
    ),
    url(
        'professor-autocomplete/$',
        AutocompleteProfessor.as_view(),
        name='professor-autocomplete',
    ),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'mynota.views.index', name='index'),
    url(r'^home/$', 'mynota.views.home', name='home' ),
    url(r'^entrar/$', 'mynota.views.entrar', name='entrar'),
    url(r'^sair/$', 'mynota.views.sair', name='sair' ),
    url(r'^aluno/detalhes/(?P<id>\d+)/$', 'mynota.views.aluno_detail', name='aluno_detail'),
    url(r'^aula/add/$', 'mynota.views.aula_add', name='aula_add' ),
    url(r'^aula/(?P<id>\d+)/delete/$', 'mynota.views.aula_delete', name='aula_delete' ),
    url(r'^aulas_por_turma/(?P<turma>.+)/$', 'mynota.views.aulas_por_turma', name='aulas_por_turma' ),
    url(r'^modulos_por_turma/(?P<turma>.+)/$', 'mynota.views.modulos_por_turma', name='modulos_por_turma' ),
    url(r'^notas_da_turma/(?P<turma>.+)/$', mynota.views.notas_da_turma, name='notas_da_turma' ),
    url(r'^plano_aula/add/$', 'mynota.views.plano_aula_add', name='plano_aula_add' ),
    url(r'^planos_por_turma/(?P<turma>.+)/$', 'mynota.views.planos_por_turma', name='planos_por_turma' ),
    url(r'^filtro_turmas/(?P<opcao>.+)/$', 'mynota.views.filtro_turmas', name='filtro_turmas' ),
    url(r'^turma/detalhes/(?P<id>\d+)/$', 'mynota.views.turma_detail', name='turma_detail'),
    url(r'^notas/listar/$', mynota.views.listar_notas, name='listar_notas'),
    url(r'^notas/lancar_nota/$', mynota.views.lancar_nota, name='lancar_nota'),
)
