from models import PhotoClusterRun
from models import PhotoCluster
import traceback
import time
from datetime import datetime
import sys
from django.db import models

class DjCluster:
    def __init__(self):
        self.run = PhotoClusterRun(
            algorithm = "DJ",)

    def write_message(self, msg):
        print(msg)
        #self.run.write_message(msg)

    def set_up(self, qs, min_pts, eps):
            # Set up
            self.write_message("Setting up...")
            self.run.status = "W"
            self.min_pts = min_pts
            self.run.density_min_pts = min_pts
            self.eps = eps
            self.run.density_eps = eps
            self.run.save()
            self.run.unprocessed.add(*[photo.pk for photo in qs])
            self.write_message("Set up Clustering for %d photos..." % (qs.count(),))

    def go(self, bbox_func, debug = False):
        try:
            self.run.status = "W"
            self.run.save()

            # Let's cluster!
            count = 0
            qs_length = self.run.unprocessed.all().count()
            self.write_message("Starting Clustering %d photos..." % (qs_length,))
            while self.run.unprocessed.all().count() > 0:
                photo = self.run.unprocessed.all()[0]
                if count % 1 == 0:
                    self.write_message("%d/%d photos done, %d left, I have %d clusters" % (count, qs_length, self.run.unprocessed.all().count(), self.run.clusters.all().count()))
                nbh_count, nbh, clusters = self.dj_neighborhood(photo, bbox_func, debug)
                if nbh_count == 0:
                    pass # is noise
                elif len(clusters) > 0:
                    self.dj_join(nbh, clusters, debug) 
                else:
                    self.dj_cluster_new(nbh, debug)

                self.run.mark_processed(photo) # Just to make sure...
                count += 1

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
            nbh = []
            seen_users = []
            clusters = []
            count = candidates.order_by('username_md5').values('username_md5').distinct().count()
            print("candidates: %d, seen users: %d" % (candidates.count(), count))
            if count < self.min_pts:
                return 0, [], []
            for candidate in candidates:
                if not(candidate.username_md5 in seen_users):
                    seen_users.append(candidate.username_md5)
                try:
                    candidate_cluster = candidate.clusters.get(run = self.run)
                    if not(candidate_cluster in clusters): 
                        clusters.append(candidate_cluster)
                except models.ObjectDoesNotExist:
                    nbh.append(candidate)

            return count, nbh, clusters

        except:
            self.run.status = "F"
            self.run.save()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            for s in traceback.format_exception(exc_type, exc_value, exc_traceback):
                self.write_message(s)

            if debug:
                import pdb
                pdb.set_trace()

    def dj_join(self, nbh, clusters, debug = False):
        try:
            target_cluster = clusters[0]
            for cluster in clusters[1:]:
                target_cluster.photos.add(*[photo.pk for photo in cluster.photos.all()])
                cluster.delete()
            self.run.unprocessed.remove(*[photo.pk for photo in nbh])
            target_cluster.photos.add(*[photo.pk for photo in nbh])

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
            self.run.unprocessed.remove(*[photo.pk for photo in nbh[1:]])
            target_cluster.photos.add(*[photo.pk for photo in nbh[1:]])

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
    qs = PhotoLocationEntry.objects.all()#box_contains(135.55515242401123,34.686962336951424,135.5,34.62299551708821)

    dj.set_up(qs, 20, 0.001)
    dj.go(PhotoLocationEntry.box_contains, True)

def cleanup_test():
    from models import PhotoClusterRun
    for run in PhotoClusterRun.objects.all():
        run.delete()