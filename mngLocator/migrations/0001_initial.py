# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-15 01:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Locator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('ip', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('longitude', models.DecimalField(decimal_places=5, max_digits=10)),
                ('latitude', models.DecimalField(decimal_places=5, max_digits=10)),
            ],
        ),
    ]
