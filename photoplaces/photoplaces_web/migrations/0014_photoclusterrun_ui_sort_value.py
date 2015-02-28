# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoplaces_web', '0013_auto_20150128_0753'),
    ]

    operations = [
        migrations.AddField(
            model_name='photoclusterrun',
            name='ui_sort_value',
            field=models.IntegerField(default=0, verbose_name=b'Sort value for ui.', db_index=True),
            preserve_default=True,
        ),
    ]
