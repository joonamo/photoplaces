# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoplaces_web', '0011_auto_20150119_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='photoclusterrun',
            name='density_eps_month',
            field=models.IntegerField(null=True, verbose_name=b'Eps value of months for density based clustering', blank=True),
            preserve_default=True,
        ),
    ]
