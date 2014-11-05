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
        for cluster in self.run.clusters.all():
            x = np.concatenate((x, [e.location_x for e in cluster.normalized_entries.all()]))
            y = np.concatenate((y, [e.location_y for e in cluster.normalized_entries.all()]))
            c = np.concatenate((c, np.ones(cluster.normalized_entries.all().count()) * cluster.pk))
            center_x = np.concatenate((center_x, [cluster.normalized_centers.location_x_mean]))
            center_y = np.concatenate((center_y, [cluster.normalized_centers.location_y_mean]))

        plt.scatter(x, y, c = c, hold = True, marker = ".", linewidths = 0)
        plt.scatter(center_x, center_y, hold = True, marker = "s")

        print("showing plot...")
        plt.show()

    def update_all_cluster_centers(self):
        def worker():
            while True:
                cluster = q.get()
                self.update_normalized_center(cluster)
                print("Cluster center normalization done, %d in queue" % (q.qsize()))

                q.task_done()

        q = Queue()
        for i in xrange(2):
            t = Thread(target = worker)
            t.daemon = True
            t.start()

        for cluster in self.run.clusters.all():
            if cluster.normalized_centers_dirty:
                q.put(cluster)

        print("Everything in queue, processing...")
        q.join()
        print("Cluster center updates done!")

    def update_normalized_center(self, cluster):
        # calculate user counts
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
        normalized_set.hour_mean = cm.cycle_avg(hours, 24, weights = weights)
        normalized_set.month_mean = cm.cycle_avg(months, 12, weights = weights)

        normalized_set.save()

    def process_iteration(self):
        pass