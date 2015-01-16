import json
import time
from models import PhotoLocationEntry, PhotoCluster, PhotoClusterRun
from datetime import datetime
from vectorformats.Formats import Django, GeoJSON
from django.db.models import Count

def photos_box_contains(x0, y0, x1, y1, srid = None):
    start_time = time.clock()
    photos = PhotoLocationEntry.box_contains(x0, y0, x1, y1, srid)
    print("[%2.4f] query found %d photos" % ((time.clock() - start_time), photos.count()))

    start_time = time.clock()
    djf = Django.Django(
        geodjango = "location", 
        properties = ["photo_thumb_url", "photo_url", "photo_id"])
    geoj = GeoJSON.GeoJSON()
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
    djf = Django.Django(
        geodjango = "bounding_shape", 
        properties = [])
    geoj = GeoJSON.GeoJSON()
    out = geoj.encode(djf.decode(clusters))
    print("[%2.4f] made geojson" % (time.clock() - start_time))

    return out

def cluster_get(pk, **kwargs):
    start_time = time.clock()

    run = PhotoClusterRun.objects.get(pk = pk)
    clusters = run.clusters.all()
    print("[%2.4f] query found %d clusters" % ((time.clock() - start_time), clusters.count()))

    start_time = time.clock()
    djf = Django.Django(
        geodjango = "center", 
        properties = [])
    geoj = GeoJSON.GeoJSON()
    out = geoj.encode(djf.decode(clusters))
    print("[%2.4f] made geojson" % (time.clock() - start_time))

    return out
