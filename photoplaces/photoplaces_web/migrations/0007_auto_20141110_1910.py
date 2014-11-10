# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoplaces_web', '0006_auto_20141105_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photoclusterrun',
            name='normalized_set',
            field=models.ForeignKey(related_name='+', blank=True, to='photoplaces_web.NormalizedPhotoSet', null=True),
            preserve_default=True,
        ),
    ]
