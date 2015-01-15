# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoplaces_web', '0007_auto_20141110_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='photoclusterrun',
            name='comment',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
