# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-21 22:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0006_plan_sfdx_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='dashboard',
            field=models.CharField(blank=True, choices=[('last', 'Most Recent Build'), ('recent', '5 Most Recent Build'), ('branches', 'Latest Builds by Branch')], default=None, max_length=8, null=True),
        ),
    ]
