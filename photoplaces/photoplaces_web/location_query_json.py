import json
import time
from models import PhotoLocationEntry, PhotoCluster, PhotoClusterRun
from datetime import datetime
import vectorformats.formats.django as vf_django
import vectorformats.formats.geojson as vf_geojson
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
from random import randrange

def photos_box_contains(x0, y0, x1, y1, srid = None):
    start_time = time.clock()
    photos = PhotoLocationEntry.box_contains(x0, y0, x1, y1, srid)
    print("[%2.4f] query found %d photos" % ((time.clock() - start_time), photos.count()))

    start_time = time.clock()
    djf = vf_django.Django(
        geodjango = "location", 
        properties = ["photo_thumb_url", "photo_url", "photo_id"])
    geoj = vf_geojson.GeoJSON()
    out = geoj.encode(djf.decode(photos))
    print("[%2.4f] made geojson" % (time.clock() - start_time))

    return out

def clusters_box_contains(x0, y0, x1, y1, **kwargs):
    start_time = time.clock()

    #run = PhotoClusterRun.objects.annotate(cluster_count=Count('clusters')).filter(algorithm = "DJ", cluster_count__gt = 20)
    #clusters = PhotoCluster.box_contains(x0, y0, x1, y1, srid = kwargs.get("srid"), run_id = kwargs.get("run_id"))
    run = PhotoClusterRun.objects.get(pk = 40)
    clusters = run.clusters.all()
    print("[%2.4f] query found %d clusters" % ((time.clock() - start_time), clusters.count()))

    start_time = time.clock()
    djf = vf_django.Django(
        geodjango = "bounding_shape", 
        properties = [])
    geoj = vf_geojson.GeoJSON()
    out = geoj.encode(djf.decode(clusters))
    print("[%2.4f] made geojson" % (time.clock() - start_time))

    return out

def clustering_run_get(pk, **kwargs):
    start_time = time.clock()

    run = PhotoClusterRun.objects.get(pk = pk)
    if run.clusters.filter(stats_dirty = True).count() > 0:
        print("clustering_run_get cleanup stats")
        run.cleanup_stats()
    clusters = run.clusters.all()
    print("[%2.4f] query found %d clusters" % ((time.clock() - start_time), clusters.count()))

    start_time = time.clock()
    djf = vf_django.Django(
        geodjango_collection = ["center", "bounding_shape"],
        properties = [
        "point_count_relative",
        "points_month_1_relative",
        "points_month_2_relative",
        "points_month_3_relative",
        "points_month_4_relative",
        "points_month_5_relative",
        "points_month_6_relative",
        "points_month_7_relative",
        "points_month_8_relative",
        "points_month_9_relative",
        "points_month_10_relative",
        "points_month_11_relative",
        "points_month_12_relative",
        "pk",
        ])
    geoj = vf_geojson.GeoJSON()
    out = geoj.encode(djf.decode(clusters))
    print("[%2.4f] made geojson" % (time.clock() - start_time))

    return out

def cluster_get(pk, **kwargs):
    start_time = time.clock()

    cluster = PhotoCluster.objects.filter(pk = pk)

    djf = vf_django.Django(
        geodjango = "bounding_shape", 
        properties = [
        "point_count_relative",
        "points_month_1_relative",
        "points_month_2_relative",
        "points_month_3_relative",
        "points_month_4_relative",
        "points_month_5_relative",
        "points_month_6_relative",
        "points_month_7_relative",
        "points_month_8_relative",
        "points_month_9_relative",
        "points_month_10_relative",
        "points_month_11_relative",
        "points_month_12_relative",
        "pk",
        ])
    geoj = vf_geojson.GeoJSON()
    out = geoj.encode(djf.decode(cluster))
    print("[%2.4f] made geojson" % (time.clock() - start_time))

    return out

def cluster_get_stats(pk, **kwargs):
    cluster = PhotoCluster.objects.get(pk = pk)

    out = {}

    out["point_count_relative"] = cluster.point_count_relative
    out["point_count"] = cluster.point_count
    for i in xrange(1,13):
        field_name = ("points_month_%d" % i)
        out[field_name] = getattr(cluster, field_name)
        out[field_name] = getattr(cluster, field_name + "_relative")

    start_idx = randrange(0, max(cluster.point_count, cluster.point_count - 29))
    photos = []
    for point in cluster.photos.all()[start_idx : start_idx + min(cluster.point_count, 30)].values("photo_id", "photo_url", "photo_thumb_url", "time", "photo_title"):
        photos.append(point)
    out["photos"] = photos

    return json.dumps(out, cls=DjangoJSONEncoder)