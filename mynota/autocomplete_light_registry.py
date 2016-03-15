# -*- coding: utf-8 -*-
from dal import autocomplete
from mynota.models import Professor, Turma

class AutocompleteTurma(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Retornando lista nula para usuário não autenticado
        if not self.request.user.is_authenticated():
            return Turma.objects.none()

        qs = Turma.objects.all()

        if self.q:
            qs = qs.filter(codigo__icontains=self.q, situacao=True)

        return qs

class AutocompleteProfessor(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Retornando lista nula para usuário não autenticado
        if not self.request.user.is_authenticated():
            return Professor.objects.none()

        qs = Professor.objects.all()

        if self.q:
            qs = qs.filter(user__first_name__icontains=self.q, user__is_active=True)

        return qs
