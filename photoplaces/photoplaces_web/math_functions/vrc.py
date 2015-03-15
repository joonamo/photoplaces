import numpy as np
from cyclical_math import *

# Calinski-Harabasz Criterion
def vrc(run, N):
    all_clusters = run.clusters.all()
    all_points_x = np.array([])
    all_points_y = np.array([])
    all_points_month = np.array([])
    month_cycle = run.clusters.all()[0].photos.all()[0].normalized_entry.normalized_set.month_z_cycle_length
    cluster_means_x = []
    cluster_means_y = []
    cluster_means_month = []
    cluster_n = []

    ssw = 0.0
    for cluster in all_clusters:
        points_x = np.array([photo.location_x for photo in cluster.photos.all().normalized_entry])
        points_y = np.array([photo.location_y for photo in cluster.photos.all().normalized_entry])
        points_month = np.array([photo.month for photo in cluster.photos.all().normalized_entry])

        m_x = np.mean(points_x)
        m_y = np.mean(points_y)
        m_month = cycle_avg(points_month, month_cycle)
        ssw += np.sum((points_x - m_x) ** 2 + (points_y - m_y) ** 2 + cm.cyclical_distance(m_month, points_month, month_cycle) ** 2)

        cluster_means_x.append(m_x)
        cluster_means_y.append(m_y)
        cluster_means_month.append(m_month)
        cluster_n.append(cluster.photos.all().count())
        all_points_x = np.concatenate((all_points_x, points_x))
        all_points_y = np.concatenate((all_points_y, points_y))
        all_points_month = np.concatenate((all_points_month, points_month))

    print("ssw: %f" % ssw)

    global_mean_x = np.mean(all_points_x) 
    global_mean_y = np.mean(all_points_y)
    global_mean_month = cycle_avg(all_points_month, month_cycleh)
    cluster_means_x = np.array(cluster_means_x)
    cluster_means_y = np.array(cluster_means_y)
    cluster_means_month = np.array(cluster_means_month)
    cluster_n = np.array(cluster_n)
    ssb = np.sum(cluster_n * ((cluster_means_x - global_mean_x) ** 2 + (cluster_means_y - global_mean_y) ** 2 + cm.cyclical_distance(global_mean_month, cluster_means_month, month_cycle) ** 2))

    print("ssb: %f" % ssb)

    k = all_clusters.count()

    print("N: %d" % N)
    print("k: %d" % k)
    return (ssb / ssw) * ((N - k) / (k - 1))