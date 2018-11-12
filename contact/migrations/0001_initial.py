# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'contact_list',
            },
            bases=(models.Model,),
        ),
    ]
