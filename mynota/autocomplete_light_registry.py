# -*- coding: utf-8 -*-
import autocomplete_light
from mynota.models import Professor, Turma

class AutocompleteTurma(autocomplete_light.AutocompleteModelBase):
    attrs={
        'placeholder': 'Digite o código da turma',
        'data-autocomplete-minimum-characters': 1,
        'class': 'edits',
    }

    def choices_for_request(self):
        q = self.request.GET.get('q', '')

        choices = self.choices.all()
        if q:
            choices = choices.filter(codigo__icontains=q, situacao=True)

        return self.order_choices(choices)[0:self.limit_choices]

autocomplete_light.register(Turma, AutocompleteTurma)

class AutocompleteProfessor(autocomplete_light.AutocompleteModelBase):
    attrs={
        'placeholder': u'Digite o nome do professor',
        'data-autocomplete-minimum-characters': 1,
        'class': 'edits',
    }

    def choices_for_request(self):
        q = self.request.GET.get('q', '')

        choices = self.choices.all()
        if q:
            choices = choices.filter(user__first_name__icontains=q, user__is_active=True)

        return self.order_choices(choices)[0:self.limit_choices]

autocomplete_light.register(Professor, AutocompleteProfessor)
