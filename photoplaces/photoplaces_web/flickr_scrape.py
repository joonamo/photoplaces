# -*- coding: utf-8 -*-

from models import PhotoLocationEntry
import json
import urllib2
import sys
import re
import traceback
from Queue import Queue
from threading import Thread
from django.conf import settings
from datetime import datetime
from pprint import pprint

def flickr_to_deg(dms):
    numbers = re.compile('\d+(?:\.\d+)?')
    dms = numbers.findall(dms)
    return float(dms[0]) + float(dms[1]) / 60.0 + float(dms[2]) / 3600.0

def flickr_date_to_datetime(t):
    return datetime.strptime(t, "%Y-%m-%d %H:%M:%S")

def process_photo(photo):
    try:
        info_url = "https://api.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key=" + settings.FLICKR_API_KEY + "&format=json&nojsoncallback=1&photo_id=" + photo["id"]
        info = json.load(urllib2.urlopen(info_url))
        lat = info["photo"]["location"]["latitude"]
        lon = info["photo"]["location"]["longitude"] 

        if PhotoLocationEntry.objects.filter(photo_id = photo["id"] + "_" + photo["secret"]).count() == 0:
            e = PhotoLocationEntry.create_flickr_entry(
                "POINT(" + str(lon) + " " + str(lat) + ")", 
                photo["owner"], 
                photo["id"],
                photo["secret"], 
                photo["farm"],
                int(photo["server"]),
                flickr_date_to_datetime(info["photo"]["dates"]["taken"]), 
                photo["title"],
                [tag["_content"] for tag in info["photo"]["tags"]["tag"]])
            print("saving " + photo["title"])
        else:
            print(photo["title"] + " aleready in db")

    except urllib2.HTTPError as e:
        if e.code != 2:
            print("HTTPError: error code " + e.code + "\n" + e.reason)
    except:
        print("Exception: " + str(sys.exc_info()[0]))
        traceback.print_exc()


def scarape_bbox(x0, y0, x1, y1, min_year):
    url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=" + settings.FLICKR_API_KEY + "&sort=relevance&media=photos&format=json&nojsoncallback=1&per_page=500&bbox=" + str(min(x0, x1)) + "," + str(min(y0, y1)) + "," + str(max(x0, x1)) + "," + str(max(y0, y1)) + "&min_upload_date=" + str(min_year)
    result = json.load(urllib2.urlopen(url))

    def worker():
        while True:
            photo = q.get()
            process_photo(photo)
            q.task_done()

    q = Queue()
    for i in range(8):
         t = Thread(target=worker)
         t.daemon = True
         t.start()

    for photo in result["photos"]["photo"]:
        q.put(photo)

    q.join()

def scrape_test(tags):
    url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=" + settings.FLICKR_API_KEY + "&tags=" + tags + "&sort=relevance&media=photos&format=json&nojsoncallback=1"
    result = json.load(urllib2.urlopen(url))
    print("Got images")
    for photo in result["photos"]["photo"]:
        try:
            exif_url = "https://api.flickr.com/services/rest/?method=flickr.photos.getExif&api_key=" + settings.FLICKR_API_KEY + "&format=json&nojsoncallback=1&photo_id=" + photo["id"]
            exif = json.load(urllib2.urlopen(exif_url))
            if "code" in exif:
                print exif["message"]
                continue
            lat = None
            lon = None
            for tag in exif ["photo"]["exif"]:
                if tag["label"] == "GPS Latitude":
                    lat = flickr_to_deg(tag["raw"]["_content"])
                elif tag["label"] == "GPS Longitude":
                    lon = flickr_to_deg(tag["raw"]["_content"])
                if bool(lat) and bool(lon):
                    break

            if not(bool(lat) and bool(lon)):
                continue

            if PhotoLocationEntry.objects.filter(photo_id = photo["id"] + "_" + photo["secret"]).count() == 0:
                e = PhotoLocationEntry.create_flickr_entry(
                    "POINT(" + str(lon) + " " + str(lat) + ")", 
                    photo["owner"], 
                    photo["id"],
                    photo["secret"], 
                    photo["farm"],
                    int(photo["server"]))
                print("saving " + photo["title"])
                e.save()
            else:
                print(photo["title"] + " aleready in db")

        except urllib2.HTTPError as e:
            if e.code != 2:
                print("error code " + e.code + "\n" + e.reason)
            continue
        except:
            print("Exception: " + str(sys.exc_info()[0]))
            traceback.print_exc()
            if raw_input("now what? ") == "q":
                break
            else:
                continue