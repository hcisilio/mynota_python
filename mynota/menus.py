# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

#submenus
aula_children = (
    MenuItem("Registrar aula ministrada",
             "/aula/add/",
             weight=10,
             icon="aula",
             check=lambda request: request.user.has_perm('mynota.add_aula')),
    MenuItem("Registrar plano de aula",
             "/plano_aula/add/",
             weight=10,
             icon="aula",
             check=lambda request: request.user.has_perm('mynota.add_planoaula')),
)

#itens do menu
Menu.add_item("main", MenuItem("Home",
                               "/",
                               weight=10,
                               icon="home",
							   check=lambda request: request.user.is_authenticated()))
Menu.add_item("main", MenuItem("Aluno",
                               "/admin/mynota/aluno/",
                               weight=10,
                               icon="aluno",
							   check=lambda request: request.user.has_perm('mynota.change_aluno')))
Menu.add_item("main", MenuItem("Professor",
                               "/admin/mynota/professor/",
                               weight=10,
                               icon="professor",
							   check=lambda request: request.user.has_perm('mynota.change_professor')))
Menu.add_item("main", MenuItem("Curso",
                               "/admin/mynota/curso/",
                               weight=10,
                               icon="curso",
							   check=lambda request: request.user.has_perm('mynota.change_curso')))
Menu.add_item("main", MenuItem("Turma",
                               "/admin/mynota/turma/",
                               weight=10,
                               icon="turma",
							   check=lambda request: request.user.has_perm('mynota.change_turma')))
# Menu.add_item("main", MenuItem("Aulas",
#                                ".",
#                                weight=10,
#                                icon="aula",
#                                children=aula_children,
# 							   check=lambda request: request.user.has_perm('mynota.add_aula')))
Menu.add_item("main", MenuItem("Aulas",
                               "/aula/add/",
                               weight=10,
                               icon="aula",
							   check=lambda request: request.user.has_perm('mynota.add_aula')))
Menu.add_item("main", MenuItem("Planos de Aula",
                               "/plano_aula/add/",
                               weight=10,
                               icon="aula",
							   check=lambda request: request.user.has_perm('mynota.add_planoaula')))
Menu.add_item("main", MenuItem("Notas",
                               "/notas/listar/",
                               weight=10,
                               icon="nota",
							   check=lambda request: request.user.has_perm('mynota.add_nota')))