from models import PhotoClusterRun
from models import PhotoCluster
import traceback
import time

class DjCluster:
    def __init__(self):
        self.run = PhotoClusterRun(
            algorithm = "DJ",)

    def write_message(self, msg):
        print(msg)
        self.run.write_message(msg)

    def go(qs, min_pts, eps, bbox_func):
        try:
            # Set up
            self.run.status = "R"
            self.min_pts = min_pts
            self.run.density_min_pts = min_pts
            self.eps = eps
            self.run.density_eps = eps
            self.run.save()

            self.write_message("Starting Clustering...")
            # Let's cluster!
            count = 0.0
            qs_length = len(qs)
            for point in qs:
                if count % 100 == 0:
                    self.write_message("%d points done, I have %d clusters", (count, len(self.run.clusters)))
                count, nbh, clusters = self.dj_neighborhood(point, bbox_func)
                if count == 0:
                    point.noise = true
                elif len(clusters) > 0:
                    self.dj_join(nbh, nbh.clusters) 
                else:
                    self.dj_cluster_new(run, nbh)

                count += 1

            self.write_message("Clustering done, found %d clusters. Starting clean up..." % (len(self.run.clusters),) )

            # cleanup clusters
            for cluster in self.run.clusters:
                cluster.update_geometry

            self.write_message("Clean up done")

            # Some housekeeping
            self.run.status = "D"
            self.run.end_time = datetime.now()
            self.run.save()

            self.write_message("All done!")
        except Exception as e:
            self.run.status = "F"
            self.run.save()
            for s in traceback.format_exception(e):
                self.write_message(s)

    def dj_neighborhood(self, point, bbox_func):
        coords = point.location.coords
        eps_half = self.eps / 2.0
        candidates = bbox_func(coords.x - eps_half, coords.y - eps_half, coords.x + eps_half, coords.y + eps_half)
        nbh = []
        seen_users = []
        clusters = []
        count = 0
        for candidate in candidates:
            if not(candidate.username_md5 in seen_users):
                seen_users.append(candidate.username_md5)
                count += 1
            if candidate.cluster != None:
                 if not(candidate.cluster in clusters): 
                    clusters.append(candidate.cluster)
            else:
                nbh.append(candidate)

        if count > self.min_pts:
            return count, nbh, clusters
        else:
            return 0, [], []

    def dj_join(self, nbh, clusters):
        target_cluster = clusters[0]
        for cluster in clusters[1:]:
            for photo in clusters:
                target_cluster.add_photo(photo)
            cluster.delete()
        for photo in nbh:
            target_cluster.add_photo(photo)

        return target_cluster

    def dj_cluster_new(self, run, nbh):
        target_cluster = PhotoCluster.create_cluster(self.run, nbh[0])
        for photo in nbh[1:]:
            target_cluster.add_photo(photo)

        return target_cluster