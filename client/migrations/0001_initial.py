# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-16 17:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeoConnected',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locator', models.CharField(max_length=100)),
                ('client', models.CharField(max_length=100)),
                ('ip', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('AS', models.CharField(max_length=100)),
                ('ISP', models.CharField(max_length=100)),
                ('longitude', models.DecimalField(decimal_places=5, max_digits=10)),
                ('latitude', models.DecimalField(decimal_places=5, max_digits=10)),
                ('latest_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='NetConnected',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locator', models.CharField(max_length=100)),
                ('client', models.CharField(max_length=100)),
                ('ip', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('AS', models.CharField(max_length=100)),
                ('ISP', models.CharField(max_length=100)),
                ('longitude', models.DecimalField(decimal_places=5, max_digits=10)),
                ('latitude', models.DecimalField(decimal_places=5, max_digits=10)),
                ('latest_update', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
