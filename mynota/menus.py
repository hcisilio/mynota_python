# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

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
                               icon="home",
							   check=lambda request: request.user.has_perm('mynota.change_professor')))
Menu.add_item("main", MenuItem("Curso",
                               "/admin/mynota/curso/",
                               weight=10,
                               icon="home",
							   check=lambda request: request.user.has_perm('mynota.change_curso')))
Menu.add_item("main", MenuItem("Turma",
                               "/admin/mynota/turma/",
                               weight=10,
                               icon="home",
							   check=lambda request: request.user.has_perm('mynota.change_turma')))
Menu.add_item("main", MenuItem("Aulas",
                               "/aula/add/",
                               weight=10,
                               icon="home",
							   check=lambda request: request.user.has_perm('mynota.add_aula')))
Menu.add_item("main", MenuItem("Planos de Aula",
                               "/plano_aula/add/",
                               weight=10,
                               icon="home",
							   check=lambda request: request.user.has_perm('mynota.add_planoaula')))
Menu.add_item("main", MenuItem("Notas",
                               "/notas/listar/",
                               weight=10,
                               icon="home",
							   check=lambda request: request.user.has_perm('mynota.add_nota')))