from django.urls import path
from django.contrib import admin
import mynota.views

admin.site.base_template = 'admin/mynota/base.html'
admin.site.base_site_template = 'admin/mynota/base_site.html'
admin.site.index_template = 'admin/mynota/index.html'
admin.site.login_template = 'admin/mynota/login.html'
admin.autodiscover()

urlpatterns = [
    #admin
    path('admin/', admin.site.urls),

    path('', mynota.views.index, name='index'),
    path('home/', mynota.views.home, name='home'),
    path('entrar/', mynota.views.entrar, name='entrar'),
    path('sair', mynota.views.sair, name='sair' ),
    path('aluno/detalhes/<int:id>/', mynota.views.aluno_detail, name='aluno_detail'),
    path('aula/add/', mynota.views.aula_add, name='aula_add' ),
    path('aula/<int:id>/delete/', mynota.views.aula_delete, name='aula_delete'),
    path('aulas_por_turma/<str:turma>/', mynota.views.aulas_por_turma, name='aulas_por_turma'),
    path('modulos_por_turma/<str:turma>/', mynota.views.modulos_por_turma, name='modulos_por_turma'),
    path('notas_da_turma/<str:turma>/', mynota.views.notas_da_turma, name='notas_da_turma'),
    path('plano_aula/add/', mynota.views.plano_aula_add, name='plano_aula_add'),
    path('planos_por_turma/(<str:turma>)/', mynota.views.planos_por_turma, name='planos_por_turma'),
    path('filtro_turmas/<str:opcao>/', mynota.views.filtro_turmas, name='filtro_turmas'),
    path('turma/detalhes/<int:id>/', mynota.views.turma_detail, name='turma_detail'),
    path('notas/listar/', mynota.views.listar_notas, name='listar_notas'),
    path('notas/lancar_nota/', mynota.views.lancar_nota, name='lancar_nota'),
    path('imprimir/<str:model>/<int:id>/', mynota.views.imprimir, name='imprimir'),
]
