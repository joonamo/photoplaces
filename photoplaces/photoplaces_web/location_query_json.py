import json
import time
from models import PhotoLocationEntry as ple
from datetime import datetime
from django.core import serializers
from vectorformats.Formats import Django, GeoJSON

def photos_box_contains(x0, y0, x1, y1, srid = None):
    start_time = time.clock()
    photos = ple.box_contains(x0, y0, x1, y1, srid)
    print("[%2.4f] query found %d photos" % ((time.clock() - start_time), len(photos)))
    start_time = time.clock()
    ret_tbl = []
    for photo in photos:
        info = {}
        info["x"] = photo.location.coords[0]
        info["y"] = photo.location.coords[1]
        info["thumb_url"] = photo.photo_thumb_url
        info["url"] = photo.photo_url
        info["photo_id"] = photo.photo_id
        ret_tbl.append(info)
    out = json.dumps(ret_tbl)
    print("[%2.4f] made old json" % (time.clock() - start_time))

    start_time = time.clock()
    djf = Django.Django(
        geodjango = "location", 
        properties = ["photo_thumb_url", "photo_url", "photo_id"])
    geoj = GeoJSON.GeoJSON()
    string = geoj.encode(djf.decode(photos))
    print("[%2.4f] made geojson" % (time.clock() - start_time))

    return out