# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-17 12:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mynota', '0002_auto_20160311_1540'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='nota',
            unique_together=set([('aluno', 'modulo')]),
        ),
    ]