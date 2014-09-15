from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
import hashlib

# Create your models here.
class PhotoLocationEntry(models.Model):
    # Geometry
    location = models.PointField()
    objects = models.GeoManager()

    # Metadata
    username_md5 = models.CharField(
        max_length = 32)
    photo_service = models.CharField(
        max_length = 1,
        choices = (('F', 'flickr'),))
    photo_id = models.CharField(
        "Photo id in service", 
        max_length = 32)
    flickr_farm_id = models.IntegerField(
        blank = True, 
        null = True)
    flickr_server_id = models.IntegerField(
        blank = True, 
        null = True)
    photo_url = models.URLField()
    photo_thumb_url = models.URLField()
    time = models.DateTimeField(
        blank = True,
        null = True)

    # Helper for creating a flickr entry. Remeber to save!
    # Args: 
    #   location, WKT: 'POINT(60.186161 24.8318864)'
    #   user, string
    #   id, string
    #   secret, string
    #   farm, int
    #   server, int
    #
    # Returns: PhotoLocationEntry
    @staticmethod
    def create_flickr_entry(location, user, id, secret, farm, server):
        photo_id = str(id) + "_" + str(secret)
        url_body = "https://farm" + str(farm) + ".staticflickr.com/" + str(server) + "/" + photo_id
        return PhotoLocationEntry(
            location = GEOSGeometry(location),
            username_md5 = hashlib.md5(user).hexdigest(),
            photo_service = "F",
            photo_id = photo_id,
            flickr_farm_id = farm,
            flickr_server_id = server,
            photo_url = url_body + ".jpg",
            photo_thumb_url = url_body + "_t.jpg")

    @staticmethod
    def box_contains(x0, y0, x1, y1, srid = None):
        if srid == None:
            srid = 4326 # WGS84!

        wkt = "POLYGON((" + \
            str(x0) + " " + str(y0) + ", "+\
            str(x0) + " " + str(y1) + ", "+\
            str(x1) + " " + str(y1) + ", "+\
            str(x1) + " " + str(y0) + ", "+\
            str(x0) + " " + str(y0) + "))"
        box = GEOSGeometry(wkt, srid)
        return PhotoLocationEntry.objects.filter(location__contained = box)