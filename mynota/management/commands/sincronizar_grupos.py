# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group

class Command(BaseCommand):

    def handle(self, *args, **options):
        group = Group.objects.get_or_create(name='Aluno')
        if group[0]:
            group = group[0]
        group = Group.objects.get_or_create(name='Diretor')
        if group[0]:
            group = group[0]
        group = Group.objects.get_or_create(name='Professor')
        if group[0]:
            group = group[0]
