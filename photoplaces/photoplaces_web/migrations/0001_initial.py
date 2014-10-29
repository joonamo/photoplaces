# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NormalizedPhotoEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location_x', models.FloatField(null=True, blank=True)),
                ('location_y', models.FloatField(null=True, blank=True)),
                ('month', models.FloatField(null=True, blank=True)),
                ('hour', models.FloatField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NormalizedPhotoSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location_x_mean', models.FloatField(null=True, blank=True)),
                ('location_x_deviation', models.FloatField(null=True, blank=True)),
                ('location_y_mean', models.FloatField(null=True, blank=True)),
                ('location_y_deviation', models.FloatField(null=True, blank=True)),
                ('month_mean', models.FloatField(null=True, blank=True)),
                ('month_deviation', models.FloatField(null=True, blank=True)),
                ('hour_mean', models.FloatField(null=True, blank=True)),
                ('hour_deviation', models.FloatField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhotoCluster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('center', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('center_dirty', models.BooleanField(default=True, db_index=True)),
                ('bounding_shape', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('bounding_shape_dirty', models.BooleanField(default=True, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhotoClusterRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('algorithm', models.CharField(max_length=2, choices=[(b'DJ', b'DJ-Cluster')])),
                ('start_time', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('end_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default=b'W', max_length=1, db_index=True, choices=[(b'W', b'Waiting'), (b'R', b'Running'), (b'D', b'Done'), (b'F', b'Failed')])),
                ('messages', models.TextField()),
                ('density_eps', models.FloatField(null=True, verbose_name=b'Eps value for density based clustering', blank=True)),
                ('density_min_pts', models.IntegerField(null=True, verbose_name=b'MinPts value for density based clustering', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhotoLocationEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('username_md5', models.CharField(max_length=32, db_index=True)),
                ('photo_service', models.CharField(max_length=1, choices=[(b'F', b'flickr')])),
                ('photo_id', models.CharField(max_length=32, verbose_name=b'Photo id in service')),
                ('flickr_farm_id', models.IntegerField(null=True, blank=True)),
                ('flickr_server_id', models.IntegerField(null=True, blank=True)),
                ('photo_url', models.URLField()),
                ('photo_thumb_url', models.URLField()),
                ('time', models.DateTimeField(null=True, blank=True)),
                ('photo_title', models.CharField(default=b'', max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhotoTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='photolocationentry',
            name='tags',
            field=models.ManyToManyField(related_name='photos', to='photoplaces_web.PhotoTag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photoclusterrun',
            name='unprocessed',
            field=models.ManyToManyField(related_name='+', to='photoplaces_web.PhotoLocationEntry'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocluster',
            name='photos',
            field=models.ManyToManyField(related_name='clusters', to='photoplaces_web.PhotoLocationEntry'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocluster',
            name='run',
            field=models.ForeignKey(related_name='clusters', to='photoplaces_web.PhotoClusterRun'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='normalizedphotoentry',
            name='actual_photo',
            field=models.ForeignKey(related_name='+', to='photoplaces_web.PhotoLocationEntry'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='normalizedphotoentry',
            name='normalized_set',
            field=models.ForeignKey(related_name='entries', to='photoplaces_web.NormalizedPhotoSet'),
            preserve_default=True,
        ),
    ]
