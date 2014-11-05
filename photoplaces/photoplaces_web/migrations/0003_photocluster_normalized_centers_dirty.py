# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoplaces_web', '0002_auto_20141103_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='photocluster',
            name='normalized_centers_dirty',
            field=models.BooleanField(default=True, db_index=True),
            preserve_default=True,
        ),
    ]
