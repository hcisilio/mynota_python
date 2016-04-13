# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    PERM_ALUNO = [
    ]
    PERM_DIRETOR = [
        'can add aluno', 'can change aluno', 'can delete aluno',
        'can add curso', 'can change curso', 'can delete curso',
        'can add modulo', 'can change modulo', 'can delete modulo',
        'can add professor', 'can change professor', 'can delete professor',
        'can add turma', 'can change turma', 'can delete turma',
        'can add nota', 'can change nota', 'can delete nota',
        'can add plano de aula', 'can change plano de aula', 'can delete plano de aula',
        'can add aula', 'can change aula', 'can delete aula',
    ]
    PERM_PROFESSOR = [
        'can change turma',
        'can add nota',
        'can add plano de aula',
        'can add aula',
    ]
    PERM_SECRETARIO = [
        'can add aluno', 'can change aluno', 'can delete aluno',
        'can add turma', 'can change turma', 'can delete turma',
    ]
    
    GROUPS = {
        'Aluno': PERM_ALUNO,
        'Diretor': PERM_DIRETOR,
        'Professor': PERM_PROFESSOR,
        'Secretario': PERM_SECRETARIO,
    }

    def handle(self, *args, **options):
        for group_name in self.GROUPS.keys():
            group = Group.objects.get_or_create(name=group_name)
            if group[0]:
                group = group[0]
            for permissao in self.GROUPS[group_name]:
                group.permissions.add(Permission.objects.get(name=permissao))
            group.save()