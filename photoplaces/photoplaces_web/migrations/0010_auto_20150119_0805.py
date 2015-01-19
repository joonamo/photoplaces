# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoplaces_web', '0009_auto_20150119_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photocluster',
            name='point_count_relative',
            field=models.FloatField(default=1.0, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photocluster',
            name='stats_dirty',
            field=models.BooleanField(default=True, db_index=True),
            preserve_default=True,
        ),
    ]
