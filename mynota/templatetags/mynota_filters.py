# -*- coding: utf-8 -*-
from django import template
from mynota.models import Nota

register = template.Library()

@register.filter
def get_nota(aluno, modulo):
    try:
        return Nota.objects.get(aluno=aluno, modulo=modulo).valor
    except Nota.DoesNotExist:
        return 0.0