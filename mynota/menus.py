# -*- coding: utf-8 -*-
from django.urls import reverse
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
                               icon="fas fa-home",
							   check=lambda request: request.user.is_authenticated))
Menu.add_item("main", MenuItem("Aluno",
                               "/admin/mynota/aluno/",
                               weight=10,
                               icon="fas fa-user-graduate",
							   check=lambda request: request.user.has_perm('mynota.change_aluno')))
Menu.add_item("main", MenuItem("Professor",
                               "/admin/mynota/professor/",
                               weight=10,
                               icon="fas fa-chalkboard-teacher",
							   check=lambda request: request.user.has_perm('mynota.change_professor')))
Menu.add_item("main", MenuItem("Curso",
                               "/admin/mynota/curso/",
                               weight=10,
                               icon="fas fa-file-certificate",
							   check=lambda request: request.user.has_perm('mynota.change_curso')))
Menu.add_item("main", MenuItem("Turma",
                               "/admin/mynota/turma/",
                               weight=10,
                               icon="fas fa-users-class",
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
                               icon="fas fa-chalkboard",
							   check=lambda request: request.user.has_perm('mynota.add_aula')))
Menu.add_item("main", MenuItem("Planos de Aula",
                               "/plano_aula/add/",
                               weight=10,
                               icon="fas fa-tasks",
							   check=lambda request: request.user.has_perm('mynota.add_planoaula')))
Menu.add_item("main", MenuItem("Notas",
                               "/notas/listar/",
                               weight=10,
                               icon="fas fa-plus-square",
							   check=lambda request: request.user.has_perm('mynota.add_nota')))
