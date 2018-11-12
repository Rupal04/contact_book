# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20181112_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactlist',
            name='number',
            field=models.BigIntegerField(max_length=20),
            preserve_default=True,
        ),
    ]
