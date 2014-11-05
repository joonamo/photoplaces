# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoplaces_web', '0003_photocluster_normalized_centers_dirty'),
    ]

    operations = [
        migrations.AddField(
            model_name='normalizedphotoset',
            name='hour_mean_natural',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='normalizedphotoset',
            name='month_mean_natural',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocluster',
            name='normalized_set',
            field=models.OneToOneField(related_name='+', null=True, blank=True, to='photoplaces_web.NormalizedPhotoSet'),
            preserve_default=True,
        ),
    ]
