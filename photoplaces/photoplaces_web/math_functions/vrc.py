import numpy as np

def vrc(run):
    all_clusters = run.clusters.all()
    all_points_x = np.array([])
    all_points_y = np.array([])
    cluster_means_x = []
    cluster_means_y = []
    cluster_n = []

    ssw = 0.0
    for cluster in all_clusters:
        points_x = np.array([photo.location[0] for photo in cluster.photos.all()])
        points_y = np.array([photo.location[1] for photo in cluster.photos.all()])

        m_x = np.mean(points_x)
        m_y = np.mean(points_y)
        ssw += np.sum((points_x - m_x) ** 2 + (points_y - m_y) ** 2)

        cluster_means_x.append(m_x)
        cluster_means_y.append(m_y)
        cluster_n.append(cluster.photos.all().count())
        all_points_x = np.concatenate((all_points_x, points_x))
        all_points_y = np.concatenate((all_points_y, points_y))

    print("ssw: %f" % ssw)

    global_mean_x = np.mean(all_points_x) 
    global_mean_y = np.mean(all_points_y) 
    cluster_means_x = np.array(cluster_means_x)
    cluster_means_y = np.array(cluster_means_y)
    cluster_n =  np.array(cluster_n)
    ssb = np.sum(cluster_n * ((cluster_means_x - global_mean_x) ** 2 + (cluster_means_y - global_mean_y) ** 2))

    print("ssb: %f" % ssb)

    N = len(all_points_x)
    k = all_clusters.count()

    print("N: %d" % N)
    print("k: %d" % k)
    return (ssb / ssw) * ((N - k) / (k / 1))