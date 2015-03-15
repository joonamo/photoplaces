# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoplaces_web', '0014_photoclusterrun_ui_sort_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='normalizedphotoentry',
            name='actual_photo',
            field=models.ForeignKey(related_name='normalized_entry', to='photoplaces_web.PhotoLocationEntry'),
            preserve_default=True,
        ),
    ]
