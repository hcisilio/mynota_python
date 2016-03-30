# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from mynota.models import Aluno, Aula, Curso, Dia, Modulo, Nota, PlanoAula, Professor, Turma

class Command(BaseCommand):

    def get_connection(self):
        import MySQLdb
        return MySQLdb.connect(
                host='localhost',
                user='root',
                passwd='root',
                db='MyNota',
                charset="utf8",
            )
    
    def importar_turmas(self):
        CURSOS = {1: 'DEVWEB', 2: 'personal', 3: 'Excel VIP'}
        sql = """
                SELECT id, curso, professor, status FROM turmas;
        """
        cur = self.get_connection().cursor()
        cur.execute(sql)
        row = cur.fetchone()
        while row:
            if not Turma.objects.filter(codigo=row[0]):
                turma = Turma(
                    codigo = row[0],
                    curso = Curso.objects.get(codigo=CURSOS[row[1]]),
                    professor = Professor.objects.get(username=row[2]),
                    situacao = row[3]
                )
                turma.save()
            row = cur.fetchone()

    def importar_dias_turmas(self):
        sql = """
                SELECT * FROM turma_dia;
        """
        cur = self.get_connection().cursor()
        cur.execute(sql)
        row = cur.fetchone()
        while row:
            turma = Turma.objects.get(codigo=row[0])
            turma.dia.add(Dia.objects.get(pk=row[1]))
            turma.save()
            row = cur.fetchone()

    def importar_planos_aulas(self):
        sql = """
                SELECT turma, modulos.nome, professor, data, conteudo FROM planos_aula
                INNER JOIN modulos ON planos_aula.modulo = modulos.id
        """
        cur = self.get_connection().cursor()
        cur.execute(sql)
        row = cur.fetchone()
        while row:
            if not PlanoAula.objects.filter(turma=Turma.objects.get(codigo=row[0]), data=row[3]):
                plano = PlanoAula (
                    turma=Turma.objects.get(codigo=row[0]),
                    modulo = Modulo.objects.get(nome=row[1]),
                    professor = Professor.objects.get(username=row[2]),
                    data=row[3],
                    conteudo=row[4]
                )
                plano.save()
            row = cur.fetchone()
    
    def importar_aulas(self):
        sql = """
                SELECT * FROM aulas
        """
        cur = self.get_connection().cursor()
        cur.execute(sql)
        row = cur.fetchone()
        while row:
            if not Aula.objects.filter(turma=Turma.objects.get(codigo=row[1]), data=row[3]):
                aula = Aula (
                    turma=Turma.objects.get(codigo=row[1]),
                    professor = Professor.objects.get(username=row[2]),
                    data=row[3],
                    conteudo=row[4]
                )
                aula.save()
            row = cur.fetchone()

    def importar_alunos(self):
        sql = """
                SELECT * FROM alunos;
        """
        cur = self.get_connection().cursor()
        cur.execute(sql)
        row = cur.fetchone()
        while row:
            if not Aluno.objects.filter(matricula=row[0]):
                nome = row[1].split()[0]
                sobrenome = ''
                for s in row[1].split()[1:]:
                    sobrenome += s + ' '
                aluno = Aluno(
                    matricula=row[0],
                    nome=nome,
                    sobrenome=sobrenome,
                    email='null@null'
                )
                aluno.save()
            row = cur.fetchone()

    def importar_matricula_turma(self):
        sql = """
                SELECT * FROM aluno_turma;
        """
        cur = self.get_connection().cursor()
        cur.execute(sql)
        row = cur.fetchone()
        while row:
            aluno = Aluno.objects.get(matricula=row[0])
            turma = Turma.objects.get(codigo=row[1])
            turma.aluno_set.add(aluno)
            turma.save()
            row = cur.fetchone()

    def importar_notas(self):
        sql = """
                SELECT aluno, modulos.nome, nota FROM notas
                INNER JOIN modulos ON notas.modulo = modulos.id;
        """
        cur = self.get_connection().cursor()
        cur.execute(sql)
        row = cur.fetchone()
        while row:
            if not Nota.objects.filter(aluno=Aluno.objects.get(matricula=row[0]), modulo=Modulo.objects.get(nome=row[1])):
                nota = Nota(
                    aluno=Aluno.objects.get(matricula=row[0]),
                    modulo=Modulo.objects.get(nome=row[1]),
                    valor=row[2]
                )
                nota.save()
            row = cur.fetchone()

    def handle(self, *args, **options):
        # self.imortar_turmas()
        # self.importar_dias_turmas()
        # self.importar_planos_aulas()
        # self.importar_aulas()
        # self.importar_alunos()
        # self.importar_matricula_turma()
        self.importar_notas()
        