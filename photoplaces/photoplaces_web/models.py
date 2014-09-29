from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, MultiPoint
import hashlib
from django.db import IntegrityError

# Create your models here.
class PhotoLocationEntry(models.Model):
    # Geometry
    location = models.PointField(spatial_index = True)
    objects = models.GeoManager()

    # Metadata
    username_md5 = models.CharField(
        max_length = 32,
        db_index = True)
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
    photo_title = models.CharField(
        default = "",
        max_length = 100)
    tags = models.ManyToManyField(
        "PhotoTag",
        related_name = "photos")
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
    def create_flickr_entry(location, user, id, secret, farm, server, time, title, tags):
        photo_id = str(id) + "_" + str(secret)
        url_body = "https://farm" + str(farm) + ".staticflickr.com/" + str(server) + "/" + photo_id
        entry = PhotoLocationEntry(
            location = GEOSGeometry(location),
            username_md5 = hashlib.md5(user).hexdigest(),
            photo_service = "F",
            photo_id = photo_id,
            flickr_farm_id = farm,
            flickr_server_id = server,
            photo_url = url_body + ".jpg",
            photo_thumb_url = url_body + "_t.jpg",
            time = time,
            photo_title = title)
        entry.save()
        for tag in tags:
            t = PhotoTag.get(tag)
            entry.tags.add(t)
        return entry

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

class PhotoTag(models.Model):
    name = models.CharField(
        max_length = 255,
        unique = True)

    @staticmethod
    def get(name):
        name = name.lower()
        try:
            return PhotoTag.objects.get(name=name)
        except models.ObjectDoesNotExist:
            try:
                tag = PhotoTag(name = name)
                tag.save()
                return tag
            except IntegrityError:
                return PhotoTag.objects.get(name=name)

class PhotoClusterRun(models.Model):
    algorithm = models.CharField(
        max_length = 2,
        choices = (('DJ', 'DJ-Cluster'),))
    start_time = models.DateTimeField(
        auto_now_add = True,
        db_index = True)
    end_time = models.DateTimeField(
        blank = True)
    status = models.CharField(
        max_length = 1,
        choices = (('R', 'Running'), ('D', 'Done'), ('F', 'Failed')),
        db_index = True)
    messages = models.TextField()
    density_eps = models.FloatField(
        "Eps value for density based clustering",
        blank = True,
        null = True)
    density_min_pts = models.IntegerField(
        "MinPts value for density based clustering",
        blank = True,
        null = True)

    def write_message(self, m):
        self.messages += datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ") + str(m) + "\n"
        self.save()

class PhotoCluster(models.Model):
    run = models.ForeignKey(
        PhotoClusterRun,
        related_name = "clusters")
    photos = models.ManyToManyField(
        PhotoLocationEntry,
        related_name = "clusters")

    # Geometry
    center = models.PointField()
    center_dirty = models.BooleanField(
        default = True,
        db_index = True)
    bounding_shape = models.PolygonField()
    bounding_shape_dirty = models.BooleanField(
        default = True,
        db_index = True)
    objects = models.GeoManager()

    @staticmethod
    def create_cluster(run, first_photo):
        c = PhotoCluster(
            run = run,
            center = first_photo.location,
            bounding_shape = GEOSGeometry("POLYGON(EMPTY)"))
        c.save()
        c.photos.add(first_photo)

    def update_center(self):
        self.center = MultiPoint([e.location for e in self.objects]).centroid
        self.center_dirty = False
        self.save()
        return self.center

    def update_bounding_shape(self):
        self.bounding_shape = MultiPoint([e.location for e in self.objects]).convex_hull
        self.bounding_shape_dirty = False
        self.save()
        return self.bounding_shape

    