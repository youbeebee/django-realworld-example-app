# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2022-03-21 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_auto_20220320_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='title',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
