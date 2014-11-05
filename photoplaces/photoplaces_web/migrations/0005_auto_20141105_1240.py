# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoplaces_web', '0004_auto_20141105_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photocluster',
            name='normalized_set',
        ),
        migrations.AddField(
            model_name='photoclusterrun',
            name='normalized_set',
            field=models.OneToOneField(related_name='+', null=True, blank=True, to='photoplaces_web.NormalizedPhotoSet'),
            preserve_default=True,
        ),
    ]
