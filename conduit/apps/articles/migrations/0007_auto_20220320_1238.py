# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2022-03-20 12:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20220320_1227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='history',
            old_name='request',
            new_name='req',
        ),
    ]
