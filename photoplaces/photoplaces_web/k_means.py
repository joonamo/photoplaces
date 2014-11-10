from models import *
import traceback
import time
from datetime import datetime
import sys
from django.db import models
import numpy as np
import math_functions.cyclical_math as cm
import matplotlib.pyplot as plt
from Queue import Queue
from threading import Thread
import math_functions.normalization as norm
from django.forms.models import model_to_dict

class KMeans:
    def __init__(self, run = None):
        if run:
            self.run = run
        else:
            self.run = PhotoClusterRun(
                algorithm = "KM")

    def write_message(self, msg):
        print(msg)
        #self.run.write_message(msg)

    def set_up(self, qs, k):
        # Set up
        self.write_message("Setting up...")
        self.run.status = "W"
        self.run.save()

        cluster_size = qs.count() / k
        print("Creating %d clusters with %d entries..." % (k, cluster_size))
        for i in xrange(k):
            first = qs[i * cluster_size]
            cluster = PhotoCluster.create_cluster(
                self.run,
                first.actual_photo,
                first)
            cluster.add_normalized_entries(qs[i * cluster_size + 1 : (i + 1) * cluster_size])
            print("%4d/%4d clusters created" % (i, k))

        print("Clusters created and values added, updating centers...")
        self.update_all_cluster_centers()
        print("Set up done")

    def simple_visualization(self):
        x = np.array([])
        y = np.array([])
        c = np.array([])
        center_x = np.array([])
        center_y = np.array([])
        center_c = np.array([])
        center_month = np.array([])
        for cluster in self.run.clusters.all().prefetch_related("normalized_entries", "normalized_centers"):
            normalized_entries = cluster.normalized_entries.all().values()
            x = np.concatenate((x, [e["location_x"] for e in normalized_entries]))
            y = np.concatenate((y, [e["location_y"] for e in normalized_entries]))
            c = np.concatenate((c, np.ones(len(normalized_entries)) * cluster.pk))
            center_x = np.concatenate((center_x, [cluster.normalized_centers.location_x_mean]))
            center_y = np.concatenate((center_y, [cluster.normalized_centers.location_y_mean]))
            center_c = np.concatenate((center_c, [cluster.pk]))
            center_month = np.concatenate((center_month, [cluster.normalized_centers.month_mean_natural]))


        plt.scatter(x, y, c = c, hold = True, marker = ".", linewidths = 0)
        plt.scatter(center_x, center_y, c = center_c, hold = True, marker = "s")
        # for i in xrange(len(center_x)):
        #     plt.text(center_x[i], center_y[i], np.floor(center_month[i]))

        print("showing plot...")
        plt.show()

    def update_all_cluster_centers(self, **kwargs):
        def worker():
            while True:
                cluster = q.get()
                self.update_normalized_center(cluster)
                print("Cluster center normalization done, %d in queue" % (q.qsize()))

                q.task_done()

        q = Queue()
        for i in xrange(3):
            t = Thread(target = worker)
            t.daemon = True
            t.start()

        force = kwargs.get("force")
        all_clusters = kwargs.get("all_clusters")
        if all_clusters is None:
            all_clusters = self.run.clusters.all().prefetch_related("photos", "normalized_entries", "normalized_centers")
        for cluster in all_clusters:
            if cluster.normalized_centers_dirty or force:
                q.put(cluster)

        print("Everything in queue, processing...")
        q.join()
        print("Cluster center updates done!")

    def update_normalized_center(self, cluster):
        # calculate user counts
        if len(cluster.normalized_entries.all()) == 0:
            return

        user_counts = {}
        distinct_users = cluster.photos.order_by('username_md5').values('username_md5').distinct()
        for user in distinct_users:
            user = user["username_md5"]
            user_counts[user] = cluster.photos.filter(username_md5 = user).count()

        normalized_entries = cluster.normalized_entries.all().values()
        entries = cluster.photos.all().values()
        weights = np.array([1.0 / user_counts[e["username_md5"]] for e in entries])
        location_xs = np.array([e["location_x"] for e in normalized_entries])
        location_ys = np.array([e["location_y"] for e in normalized_entries])
        hours = np.array([e["time"].hour for e in entries])
        months = np.array([e["time"].month for e in entries])

        if not cluster.normalized_centers:
            c = NormalizedPhotoSet()
            c.save()
            cluster.normalized_centers = c
            cluster.save()

        normalized_set = cluster.normalized_centers
        normalized_set.location_x_mean = np.average(location_xs, weights = weights)
        normalized_set.location_y_mean = np.average(location_ys, weights = weights)
        
        normalized_set.hour_mean_natural = cm.cycle_avg(hours, 24, weights = weights)
        normalized_set.hour_mean = norm.cyclical_z_score(
            normalized_set.hour_mean_natural,
            self.run.normalized_set.hour_mean,
            self.run.normalized_set.hour_deviation,
            24)
        
        normalized_set.month_mean_natural = cm.cycle_avg(months, 12, weights = weights)
        normalized_set.month_mean = norm.cyclical_z_score(
            normalized_set.month_mean,
            self.run.normalized_set.month_mean,
            self.run.normalized_set.month_deviation,
            12)

        cluster.normalized_centers_dirty = False

        normalized_set.save()
        cluster.save()

    def process_iteration(self, **kwargs):
        normalized_entries = kwargs.get("normalized_entries")
        add_normalized_entreis_from_clusters = False
        if normalized_entries is None:
            normalized_entries = []
            add_normalized_entreis_from_clusters = True

        print ("Querying clusters...")
        cluster_centers = []
        cluster_map = {}
        all_clusters = kwargs.get("all_clusters")
        if all_clusters is None:
            all_clusters = self.run.clusters.all().prefetch_related("normalized_centers", "normalized_entries", "photos")
        print("iterating clusters...")
        for cluster in all_clusters:
            cluster_map[cluster.id] = [[],[]] 
            d = model_to_dict(cluster.normalized_centers)
            d["cluster_id"] = cluster.pk
            cluster_centers.append(d)
            if add_normalized_entreis_from_clusters:
                normalized_entries += cluster.normalized_entries.all().values()

        print("iterating entries...")
        done = 0
        count_all = len(normalized_entries)
        month_cycle = self.run.normalized_set.month_z_cycle_length
        for entry in normalized_entries:
            lowest = float("inf")
            closest = -1
            x = entry["location_x"]
            y = entry["location_y"]
            month = entry["month"]
            for cluster in cluster_centers:
                d = norm.dist(cluster["location_x_mean"], x) ** 2 +\
                norm.dist(cluster["location_y_mean"], y) ** 2 +\
                cm.cyclical_distance(cluster["month_mean"], month, month_cycle) ** 2
                if d < lowest:
                    closest = cluster["cluster_id"]
                    lowest = d

            cluster_map[closest][0].append(entry["id"])
            cluster_map[closest][1].append(entry["actual_photo_id"])

            done += 1
            if done % 5000 == 0:
                print("%6d/%6d (%3.1f%%) processed" % (done, count_all, 100.0 * done / count_all))

        # Threads here!
        print("All processed... pushing to db...")
        count_all = self.run.clusters.count()
        
        q = Queue()
        def worker():
            while True:
                cluster = q.get()
                cluster_pk = cluster.pk
                cluster.clear_normalized_entries()
                cluster.add_normalized_entries_from_keys(*cluster_map[cluster_pk])
                try:
                    self.update_normalized_center(cluster)
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    for s in traceback.format_exception(exc_type, exc_value, exc_traceback):
                        self.write_message(s)
                    pass

                print("Added %d entries to cluster. %3d left." % (len(cluster_map[cluster.pk][0]), q.qsize()))

                q.task_done()

        for i in xrange(3):
            t = Thread(target = worker)
            t.daemon = True
            t.start()


        for cluster in all_clusters:
            q.put(cluster)
        q.join()

        print("Entries added, updating cluster centers...")
        self.update_all_cluster_centers()
        print("Iteration done!")