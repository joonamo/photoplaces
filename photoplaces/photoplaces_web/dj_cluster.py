from models import PhotoClusterRun
from models import PhotoCluster
from math_functions.cyclical_math import month_wrap
import traceback
import time
from datetime import datetime
import sys
from Queue import Queue
from threading import Thread
from django.db import models
from django.db.models import Q

class DjCluster:
    def __init__(self, **kwargs):
        run = kwargs.get("run")
        if not(run):
            self.run = PhotoClusterRun(algorithm = "DJ",)
        else:
            self.run = run
            self.min_pts = self.run.density_min_pts
            self.eps = self.run.density_eps
            eps_month = self.run.density_eps_month
            if not(eps_month):
                self.eps_month = -1
            else:
                self.eps_month = eps_month

    def write_message(self, msg):
        print(msg)
        #self.run.write_message(msg)

    def set_up(self, qs, min_pts, eps, **kwargs):
        # Set up
        self.write_message("Setting up...")
        self.run.status = "W"
        self.min_pts = min_pts
        self.run.density_min_pts = min_pts
        self.eps = eps
        self.run.density_eps = eps
        eps_month = kwargs.get("eps_month")
        if not(eps_month):
            self.eps_month = -1
        else:
            self.run.density_eps_month = eps_month
            self.eps_month = eps_month
        self.run.save()
        self.run.unprocessed.add(*[photo["id"] for photo in qs.values()])
        self.write_message("Set up Clustering for %d photos, clustering id %d..." % (qs.count(), self.run.pk))


    def go(self, bbox_func, debug = False):
        try:
            self.run.status = "W"
            self.run.save()

            # Let's cluster!
            count = 0
            qs_length = self.run.unprocessed.all().count()
            self.write_message("Starting Clustering %d photos..." % (qs_length,))
            nbh_queue = Queue()
            for photo in self.run.unprocessed.all():
                nbh_queue.put(photo)
            self.write_message("All photos in queue, starting nbh workers...")
            nbh_queue.put(None)
            join_queue = Queue()

            def nbh_worker():
                while True:
                    photo = nbh_queue.get()
                    if photo is None:
                        join_queue.put(None)
                        nbh_queue.put(None)
                        self.write_message("Nbh Worker done")
                        break
                    nbh_count, nbh = self.dj_neighborhood(photo, bbox_func, debug)
                    if nbh_count == 0:
                       self.run.mark_processed(photo)
                    else:
                        join_queue.put((photo, nbh))

            nbh_worker_count = 5
            threads = []
            for i in xrange(nbh_worker_count):
                t = Thread(target = nbh_worker)
                t.daemon = True
                t.start()
                threads.append(t)

            self.write_message("Workers started, starting join process...")
            while nbh_worker_count > 0:
                photo, nbh = join_queue.get()
                if nbh is None:
                    nbh_worker_count -= 1
                    self.write_message("Encountered none, workers left: %d" % (nbh_worker_count))
                else:
                    self.dj_join(nbh, debug)
                    self.run.mark_processed(photo)

                    count += 1

                    self.write_message("%d photos processed, %d/%d left, %d clusters found so far" % (count, self.run.unprocessed.all().count(), qs_length, self.run.clusters.all().count()))

            for thread in threads:
                print("killing thread")
                thread.join()
                print("it's gone!")

            # while self.run.unprocessed.all().count() > 0:
            #     photo = self.run.unprocessed.all()[0]
            #     nbh_count, nbh, clusters = self.dj_neighborhood(photo, bbox_func, debug)
            #     if nbh_count == 0:
            #         pass
            #     elif len(clusters) > 0:
            #         self.dj_join(nbh, clusters, debug) 
            #     else:
            #         self.dj_cluster_new(nbh, debug)

            #     self.run.mark_processed(photo)

            #     count += 1

            #     if nbh_count > 0:
            #         self.write_message("%d photos processed, %d/%d left, %d clusters found so far" % (count, self.run.unprocessed.all().count(), qs_length, self.run.clusters.all().count()))

            self.write_message("Clustering done, found %d clusters. Starting clean up..." % (self.run.clusters.all().count(),) )

            # cleanup clusters
            for cluster in self.run.clusters.all():
                cluster.update_geometry()

            self.write_message("Clean up done")

            # Some housekeeping
            self.run.status = "D"
            self.run.end_time = datetime.now()
            self.run.save()

            self.write_message("All done!")

        except:
            self.run.status = "F"
            self.run.save()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            for s in traceback.format_exception(exc_type, exc_value, exc_traceback):
                self.write_message(s)

            if debug:
                import pdb
                pdb.set_trace()

    def dj_neighborhood(self, point, bbox_func, debug = False):
        try:
            coords = point.location.coords
            eps_half = self.eps / 2.0
            candidates = bbox_func(coords[0] - eps_half, coords[1] - eps_half, coords[0] + eps_half, coords[1] + eps_half)

            if self.eps_month > -1:
                count = candidates.order_by('username_md5').values('username_md5').distinct().count()
                if count < self.min_pts:
                    #print("candidates before month filter: %d, seen users: %d" % (candidates.count(), count))
                    return 0, []

                month = point.time.month
                q = Q(time__month = month)
                for offset in xrange(1, self.eps_month + 1):
                    q = q | Q(time__month = month_wrap(month - offset)) | Q(time__month = month_wrap(month + offset))
                candidates = candidates.filter(q)
            # nbh = []
            # seen_users = []
            # clusters = []
            count = candidates.order_by('username_md5').values('username_md5').distinct().count()
            #print("candidates: %d, seen users: %d" % (candidates.count(), count))
            if count < self.min_pts:
                return 0, []
            # for candidate in candidates:
            #     if not(candidate.username_md5 in seen_users):
            #         seen_users.append(candidate.username_md5)
            #     try:
            #         candidate_cluster = candidate.clusters.get(run = self.run)
            #         if not(candidate_cluster in clusters): 
            #             clusters.append(candidate_cluster)
            #     except models.ObjectDoesNotExist:
            #         nbh.append(candidate)

            return count, candidates

        except:
            self.run.status = "F"
            self.run.save()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            for s in traceback.format_exception(exc_type, exc_value, exc_traceback):
                self.write_message(s)

            if debug:
                import pdb
                pdb.set_trace()

    def dj_join(self, nbh, debug = False):
        try:
            photos_without_clusters = []
            point_ids = nbh.values_list("pk", flat = True)
            q = Q()
            for pk in point_ids:
                q = q | Q(photos__pk = pk)
            q = q & Q(run__pk = self.run.pk)
            cluster_ids = PhotoCluster.objects.filter(q).values_list("pk", flat = True).distinct()
            # for photo in nbh:
            #     try:
            #         candidate_cluster = photo.clusters.get(run = self.run)
            #         if not(candidate_cluster in clusters): 
            #             clusters.append(candidate_cluster)
            #     except models.ObjectDoesNotExist:
            #         photos_without_clusters.append(photo)
            if len(cluster_ids) == 0:
                target_cluster = self.dj_cluster_new(nbh, debug)
            else:
                # Actual join operation
                q = Q()
                for idx in cluster_ids:
                    q = q | Q(pk = idx)
                clusters = PhotoCluster.objects.filter(q)
                target_cluster = clusters[0]
                for cluster in clusters[1:]:
                    target_cluster.photos.add(*[v for v in cluster.photos.all().values_list("pk", flat = True)])
                    cluster.delete()
                #self.run.unprocessed.remove(*[photo.pk for photo in nbh])
                target_cluster.photos.add(*[v for v in nbh.values_list("pk", flat = True)])

            return target_cluster

        except:
            self.run.status = "F"
            self.run.save()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            for s in traceback.format_exception(exc_type, exc_value, exc_traceback):
                self.write_message(s)

            if debug:
                import pdb
                pdb.set_trace()

    def dj_cluster_new(self, nbh, debug = False):
        try:
            target_cluster = PhotoCluster.create_cluster(self.run, nbh[0])
            target_cluster.photos.add(*[v for v in nbh[1:].values_list("pk", flat = True)])
            #self.run.unprocessed.remove(*[photo.pk for photo in nbh])

            return target_cluster

        except:
            self.run.status = "F"
            self.run.save()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            for s in traceback.format_exception(exc_type, exc_value, exc_traceback):
                self.write_message(s)

            if debug:
                import pdb
                pdb.set_trace()

def dj_test():
    dj = DjCluster()
    from models import PhotoLocationEntry
    #qs = PhotoLocationEntry.objects.all()
    qs = PhotoLocationEntry.box_contains(135.55515242401123,34.686962336951424,135.5,34.62299551708821)

    dj.set_up(qs, 8, 0.001, eps_month = 2)
    dj.go(PhotoLocationEntry.box_contains, True)

    return dj