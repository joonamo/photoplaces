import json
from models import PhotoLocationEntry as ple

def photos_box_contains(x0, y0, x1, y1, srid = None):
    photos = ple.box_contains(x0, y0, x1, y1, srid)
    ret_tbl = []
    for photo in photos:
        info = {}
        info["x"] = photo.location.coords[0]
        info["y"] = photo.location.coords[1]
        info["thumb_url"] = photo.photo_thumb_url
        info["url"] = photo.photo_url
        info["photo_id"] = photo.photo_id
        ret_tbl.append(info)
    return json.dumps(ret_tbl)