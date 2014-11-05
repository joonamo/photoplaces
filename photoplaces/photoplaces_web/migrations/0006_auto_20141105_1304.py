# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoplaces_web', '0005_auto_20141105_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='normalizedphotoset',
            name='hour_z_cycle_length',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='normalizedphotoset',
            name='month_z_cycle_length',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='normalizedphotoentry',
            name='hour',
            field=models.FloatField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='normalizedphotoentry',
            name='location_x',
            field=models.FloatField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='normalizedphotoentry',
            name='location_y',
            field=models.FloatField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='normalizedphotoentry',
            name='month',
            field=models.FloatField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
