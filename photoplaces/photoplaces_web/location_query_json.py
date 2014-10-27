import json
import time
from models import PhotoLocationEntry, PhotoCluster
from datetime import datetime
from vectorformats.Formats import Django, GeoJSON

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

    clusters = PhotoCluster.box_contains(x0, y0, x1, y1, srid = kwargs.get("srid"), run_id = kwargs.get("run_id"))
    print("[%2.4f] query found %d clusters" % ((time.clock() - start_time), clusters.count()))

    start_time = time.clock()
    djf = Django.Django(
        geodjango = "bounding_shape", 
        properties = [])
    geoj = GeoJSON.GeoJSON()
    out = geoj.encode(djf.decode(clusters))
    print("[%2.4f] made geojson" % (time.clock() - start_time))

    return out