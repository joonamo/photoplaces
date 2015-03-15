from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, MultiPoint, Polygon
import hashlib
from django.db import IntegrityError
from django.db.models import Count
from datetime import datetime
import _mysql_exceptions
import numpy as np

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
            photo_title = title[:100])
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

    @staticmethod
    def box_disjoint(x0, y0, x1, y1, srid = None):
        if srid == None:
            srid = 4326 # WGS84!

        wkt = "POLYGON((" + \
            str(x0) + " " + str(y0) + ", "+\
            str(x0) + " " + str(y1) + ", "+\
            str(x1) + " " + str(y1) + ", "+\
            str(x1) + " " + str(y0) + ", "+\
            str(x0) + " " + str(y0) + "))"
        box = GEOSGeometry(wkt, srid)
        return PhotoLocationEntry.objects.filter(location__disjoint = box)

class NormalizedPhotoSet(models.Model):
    location_x_mean = models.FloatField(
        blank = True, 
        null = True)
    location_x_deviation = models.FloatField(
        blank = True, 
        null = True)
    location_y_mean = models.FloatField(
        blank = True, 
        null = True)
    location_y_deviation = models.FloatField(
        blank = True, 
        null = True)

    month_mean = models.FloatField(
        blank = True, 
        null = True)
    month_deviation = models.FloatField(
        blank = True, 
        null = True)
    month_z_cycle_length = models.FloatField(
        blank = True,
        null = True)

    month_mean_natural = models.FloatField(
        blank = True, 
        null = True)
    hour_mean = models.FloatField(
        blank = True, 
        null = True)
    hour_deviation = models.FloatField(
        blank = True, 
        null = True)
    hour_mean_natural = models.FloatField(
        blank = True, 
        null = True)
    hour_z_cycle_length = models.FloatField(
        blank = True,
        null = True)

class NormalizedPhotoEntry(models.Model):
    actual_photo = models.ForeignKey(
        PhotoLocationEntry,
        related_name = "normalized_entry")
    normalized_set = models.ForeignKey(
        NormalizedPhotoSet,
        related_name = "entries")
    location_x = models.FloatField(
        blank = True, 
        null = True,
        db_index = True)
    location_y = models.FloatField(
        blank = True, 
        null = True,
        db_index = True)
    month = models.FloatField(
        blank = True, 
        null = True,
        db_index = True)
    hour = models.FloatField(
        blank = True, 
        null = True,
        db_index = True)

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
                try:
                    tag.save()
                except _mysql_exceptions.Warning:
                    pass
                return tag
            except IntegrityError:
                return PhotoTag.objects.get(name=name)

class PhotoClusterRun(models.Model):
    algorithm = models.CharField(
        max_length = 2,
        choices = (('DJ', 'DJ-Cluster'),('KM', 'K-Means'),))
    start_time = models.DateTimeField(
        auto_now_add = True,
        db_index = True)
    end_time = models.DateTimeField(
        auto_now_add = True)
    status = models.CharField(
        max_length = 1,
        choices = (("W", "Waiting"), ('R', 'Running'), ('D', 'Done'), ('F', 'Failed')),
        db_index = True,
        default = "W")
    messages = models.TextField()
    density_eps = models.FloatField(
        "Eps value for density based clustering",
        blank = True,
        null = True)
    density_eps_month = models.IntegerField(
        "Eps value of months for density based clustering",
        blank = True,
        null = True)
    density_min_pts = models.IntegerField(
        "MinPts value for density based clustering",
        blank = True,
        null = True)
    unprocessed = models.ManyToManyField(
        PhotoLocationEntry,
        related_name = "+")

    normalized_set = models.ForeignKey(
        NormalizedPhotoSet,
        related_name = "+",
        blank = True,
        null = True)
    ui_sort_value = models.IntegerField(
        "Sort value for ui.",
        db_index = True,
        default = 0)

    comment = models.TextField(
        default = "")

    def write_message(self, m):
        self.messages += datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ") + str(m) + "\n"
        self.save()

    def mark_processed(self, v):
        try:
            self.unprocessed.remove(v)
            return True
        except models.ObjectDoesNotExist:
            return False

    def update_geometry(self):
        for c in self.clusters.all():
            c.update_geometry()

    def cleanup_stats(self):
        clusters = self.clusters.annotate(photo_count = Count("photos")).order_by("-photo_count")
        max_points = clusters[0].photo_count
        for cluster in clusters:
            point_count_f = float(cluster.photo_count)
            cluster.point_count_relative =  point_count_f / max_points
            cluster.point_count = cluster.photo_count
            for i in xrange(1,13):
                points_this_month = cluster.photos.filter(time__month = i).count()
                setattr(cluster, ("points_month_%d" % i), points_this_month)
                setattr(cluster, ("points_month_%d_relative" % i), points_this_month / point_count_f)
            cluster.stats_dirty = False
            cluster.save()

    def show_some_stats(self, area_srid):
        clusters = self.clusters.annotate(photo_count = Count("photos"))
        point_counts = np.array([c.photo_count for c in clusters])
        max_points = np.max(point_counts)
        min_points = np.min(point_counts)
        avg_points = np.average(point_counts)
        median_points = np.median(point_counts)

        def get_area(cluster):
            shape = cluster.bounding_shape
            shape.transform(area_srid)
            return shape.area / (10 ** 6)
        areas = np.array([get_area(c) for c in clusters])
        max_area = np.max(areas)
        min_area = np.min(areas)
        avg_area = np.average(areas)
        median_area = np.median(areas)

        print("Total clusters: %d" % (clusters.count(), ))
        print("max_points: %d, min_points: %d, avg_points: %f, median_points: %d" % (max_points, min_points, avg_points, median_points))
        print("max_area: %f km^2, min_area: %f km^2, avg_area: %f km^2, median_area: %f km^2" % (max_area, min_area, avg_area, median_area))

class PhotoCluster(models.Model):
    run = models.ForeignKey(
        PhotoClusterRun,
        related_name = "clusters")
    photos = models.ManyToManyField(
        PhotoLocationEntry,
        related_name = "clusters")
    normalized_entries = models.ManyToManyField(
        NormalizedPhotoEntry,
        related_name = "clusters")

    normalized_centers = models.OneToOneField(
        NormalizedPhotoSet,
        related_name = "+",
        blank = True,
        null = True)
    normalized_centers_dirty = models.BooleanField(
        default = True,
        db_index = True)

    # Statistics
    stats_dirty = models.BooleanField(
        db_index = True,
        default = True)

    points_month_1 = models.IntegerField(
        default = 0)
    points_month_2 = models.IntegerField(
        default = 0)
    points_month_3 = models.IntegerField(
        default = 0)
    points_month_4 = models.IntegerField(
        default = 0)
    points_month_5 = models.IntegerField(
        default = 0)
    points_month_6 = models.IntegerField(
        default = 0)
    points_month_7 = models.IntegerField(
        default = 0)
    points_month_8 = models.IntegerField(
        default = 0)
    points_month_9 = models.IntegerField(
        default = 0)
    points_month_10 = models.IntegerField(
        default = 0)
    points_month_11 = models.IntegerField(
        default = 0)
    points_month_12 = models.IntegerField(
        default = 0)
    point_count = models.IntegerField(
        db_index = True,
        default = 1.0)

    points_month_1_relative = models.FloatField(
        default = 0)
    points_month_2_relative = models.FloatField(
        default = 0)
    points_month_3_relative = models.FloatField(
        default = 0)
    points_month_4_relative = models.FloatField(
        default = 0)
    points_month_5_relative = models.FloatField(
        default = 0)
    points_month_6_relative = models.FloatField(
        default = 0)
    points_month_7_relative = models.FloatField(
        default = 0)
    points_month_8_relative = models.FloatField(
        default = 0)
    points_month_9_relative = models.FloatField(
        default = 0)
    points_month_10_relative = models.FloatField(
        default = 0)
    points_month_11_relative = models.FloatField(
        default = 0)
    points_month_12_relative = models.FloatField(
        default = 0)
    point_count_relative = models.FloatField(
        db_index = True,
        default = 1.0)

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
    def create_cluster(run, first_photo, normalized_entry = None):
        c = PhotoCluster(
            run = run,
            center = first_photo.location,
            bounding_shape = GEOSGeometry("POLYGON((0 0, 0 0, 0 0, 0 0))"))
        c.save()
        c.photos.add(first_photo)
        if normalized_entry:
            c.normalized_entries.add(normalized_entry)

        return c

    def clear_normalized_entries(self):
        self.photos.clear()
        self.normalized_entries.clear()

    def add_normalized_entries(self, normalized_entries):
        self.add_normalized_entries_from_keys(
            [e.pk for e in normalized_entries],
            [e.actual_photo.pk for e in normalized_entries])

    def add_normalized_entries_from_keys(self, normalized_entries, actual_photos):
        self.normalized_entries.add(*[e for e in normalized_entries])
        self.photos.add(*[e for e in actual_photos])
        self.center_dirty = True
        self.bounding_shape_dirty = True
        self.normalized_centers_dirty = True
        self.stats_dirty = True
        self.save()
        return False

    def add_photo(self, photo):
        try:
            self.photos.get(pk=photo.pk)
            return True
        except models.ObjectDoesNotExist:
            self.photos.add(photo)
            self.center_dirty = True
            self.bounding_shape_dirty = True
            self.stats_dirty = True
            self.save()
            return False

    def update_geometry(self):
        self.update_center()
        self.update_bounding_shape()

    def update_center(self):
        self.center = MultiPoint([e.location for e in self.photos.all()]).centroid
        self.center_dirty = False
        self.save()
        return self.center

    def update_bounding_shape(self):
        ch = MultiPoint([e.location for e in self.photos.all()]).convex_hull
        if len(ch.coords[0]) > 2:
            self.bounding_shape = ch
        else:
            if ch.geom_typeid == 0:
                self.bounding_shape = Polygon.from_bbox((ch.coords[0], ch.coords[1], ch.coords[0], ch.coords[1]))
            else:
                self.bounding_shape = Polygon.from_bbox((ch.coords[0][0], ch.coords[0][1], ch.coords[1][0], ch.coords[1][1]))
        self.bounding_shape_dirty = False
        self.save()
        return self.bounding_shape

    @staticmethod
    def box_contains(x0, y0, x1, y1, **kwargs):
        srid = kwargs.get("srid")
        if srid == None:
            srid = 4326 # WGS84!

        run_id = kwargs.get("run_id")
        if run_id != None:
            qs = PhotoCluster.objects.filter(run = kwargs["run_id"])
        else:
            qs = PhotoCluster.objects.all()

        wkt = "POLYGON((" + \
            str(x0) + " " + str(y0) + ", "+\
            str(x0) + " " + str(y1) + ", "+\
            str(x1) + " " + str(y1) + ", "+\
            str(x1) + " " + str(y0) + ", "+\
            str(x0) + " " + str(y0) + "))"
        box = GEOSGeometry(wkt, srid)
        return qs.filter(center__contained = box)
