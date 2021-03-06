# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoplaces_web', '0008_photoclusterrun_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='photocluster',
            name='point_count_relative',
            field=models.FloatField(default=1.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocluster',
            name='points_month_1',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocluster',
            name='points_month_10',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocluster',
            name='points_month_11',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocluster',
            name='points_month_12',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocluster',
            name='points_month_2',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocluster',
            name='points_month_3',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocluster',
            name='points_month_4',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocluster',
            name='points_month_5',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocluster',
            name='points_month_6',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocluster',
            name='points_month_7',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocluster',
            name='points_month_8',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocluster',
            name='points_month_9',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocluster',
            name='stats_dirty',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
