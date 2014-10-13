# -*- coding: utf-8 -*-

from models import PhotoLocationEntry
import json
import urllib2
import sys
import re
import traceback
import time
import exceptions
from Queue import Queue
from threading import Thread, Event
from django.conf import settings
from datetime import datetime
from pprint import pprint

def flickr_to_deg(dms):
    numbers = re.compile('\d+(?:\.\d+)?')
    dms = numbers.findall(dms)
    return float(dms[0]) + float(dms[1]) / 60.0 + float(dms[2]) / 3600.0

def flickr_date_to_datetime(t):
    return datetime.strptime(t, "%Y-%m-%d %H:%M:%S")

def process_photo(photo, e):
    try:
        start_time = time.clock()    
        if PhotoLocationEntry.objects.filter(photo_id = photo["id"] + "_" + photo["secret"]).count() == 0:
            info_url = "https://api.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key=" + settings.FLICKR_API_KEY + "&format=json&nojsoncallback=1&photo_id=" + photo["id"]
            info = json.load(urllib2.urlopen(info_url))
            lat = info["photo"]["location"]["latitude"]
            lon = info["photo"]["location"]["longitude"] 

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
            print("[%2.4f] saving %s" % ((time.clock() - start_time), photo["title"]))
        else:
            print("[%2.4f] aleready in db %s" % ((time.clock() - start_time), photo["title"]))

    except exceptions.KeyError:
        pass
    except urllib2.HTTPError as e:
        if e.code != 2:
            print("HTTPError: error code " + e.code + "\n" + e.reason)
    except:
        e.clear()
        print("Exception: " + str(sys.exc_info()[0]))
        traceback.print_exc()
        raw_input("now what?")
        e.set()

def scarape_bbox(x0, y0, x1, y1, start_page, max_pages, **kwargs):
    def worker(e):
        while True:
            if not e.isSet():
                print("waiting event")
                e.wait()
            photo = q.get()
            process_photo(photo, e)
            q.task_done()

    q = Queue()
    e = Event()
    e.set()
    for i in range(8):
        t = Thread(target=worker, args=(e,))
        t.daemon = True
        t.start()

    page = start_page
    query_max_pages = 1
    while  page <= min(max_pages, query_max_pages):
        url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=" + settings.FLICKR_API_KEY + "&sort=interestingness-desc&media=photos&format=json&nojsoncallback=1&per_page=250&bbox=" + str(min(x0, x1)) + "," + str(min(y0, y1)) + "," + str(max(x0, x1)) + "," + str(max(y0, y1))  + "&page=" + str(page)
        if "min_taken_date" in kwargs:
            url += "&min_taken_date=" + str(kwargs["min_taken_date"])
        if "max_taken_date" in kwargs:
            url += "&max_taken_date=" + str(kwargs["max_taken_date"])
        print("url: %s" % url)

        result = json.load(urllib2.urlopen(url))
        query_max_pages = result["photos"]["pages"]
        for photo in result["photos"]["photo"]:
            q.put(photo)

        q.join()
        print("******************\npage %i/%i done\n******************" % (page, min(query_max_pages, max_pages)) )

        page += 1

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

def reasearch_area_scrape(month, year):
    min_taken_date = "%d-%d" % (year, month)
    if month == 12:
        month = 1
        year = year + 1
    else:
        month += 1
    max_taken_date = "%d-%d" % (year, month)
    scarape_bbox(136.3128662109375, 
        34.963622674200224,
        134.5550537109375, 
        34.19476548661921, 
        0, 
        9, 
        min_taken_date = min_taken_date, 
        max_taken_date = max_taken_date)
