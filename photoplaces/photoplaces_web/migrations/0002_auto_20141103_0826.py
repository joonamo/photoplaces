# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoplaces_web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photocluster',
            name='normalized_centers',
            field=models.OneToOneField(related_name='+', null=True, blank=True, to='photoplaces_web.NormalizedPhotoSet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocluster',
            name='normalized_entries',
            field=models.ManyToManyField(related_name='clusters', to='photoplaces_web.NormalizedPhotoEntry'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photoclusterrun',
            name='algorithm',
            field=models.CharField(max_length=2, choices=[(b'DJ', b'DJ-Cluster'), (b'KM', b'K-Means')]),
            preserve_default=True,
        ),
    ]
