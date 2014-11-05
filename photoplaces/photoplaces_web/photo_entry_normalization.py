from models import PhotoLocationEntry, NormalizedPhotoSet, NormalizedPhotoEntry
import numpy as np
from math_functions.cyclical_math import *
from math_functions.normalization import *
from Queue import Queue
from threading import Thread, Event

def visualize_counts(qs, field):
    values = qs.order_by(field).values(field).distinct()
    values = [v[field] for v in values]
    m = 20000
    for value in values:
        c = qs.filter(**{field + "__gte": value - 0.001, field + "__lte": value + 0.001}).count()
        print( ("%2.6f: %6d " % (value, c)) + "#" * int(float(c) / m * 60))

def normalize_photo_entry(entry, target_set):
    e = NormalizedPhotoEntry(
        actual_photo = entry,
        normalized_set = target_set,
        location_x = z_score(entry.location[0], target_set.location_x_mean, target_set.location_x_deviation),
        location_y = z_score(entry.location[1], target_set.location_y_mean, target_set.location_y_deviation),
        month = cyclical_z_score(entry.time.month, target_set.month_mean, target_set.month_deviation, 12),
        hour = cyclical_z_score(entry.time.hour, target_set.hour_mean, target_set.hour_deviation, 24))
    e.save()

def normalize_values(normalized_set):
    count = PhotoLocationEntry.objects.all().count()
    def worker():
        while True:
            e = q.get()
            if NormalizedPhotoEntry.objects.filter(actual_photo = e).count() == 0:
                normalize_photo_entry(e, normalized_set)
                done = NormalizedPhotoEntry.objects.all().count()
                if done % 100 == 0 or done == 1:
                    print("%d / %d (%3.1f) done" % (done, count, float(done) / count  * 100))
            q.task_done()

    q = Queue()
    for i in xrange(4):
        t = Thread(target = worker)
        t.daemon = True
        t.start()

    for v in PhotoLocationEntry.objects.all():
        q.put(v)

    print("All in Queue, waiting...")
    q.join()

    # Untested, only done in interactive console...
    hours = ns.entries.order_by("hour").values("hour").distinct()
    normalized_set.hour_z_cycle_length = abs(hours[0]["hour"] - hours[1]["hour"]) * 24
    months = ns.entries.order_by("month").values("month").distinct()
    normalized_set.month_z_cycle_length = abs(months[0]["month"] - months[1]["month"]) * 12

    print("All done")


def create_normalized_set():
    print("Getting objects...")
    values = PhotoLocationEntry.objects.all()

    print("creating NormalizedPhotoSet...")
    normalized_set = NormalizedPhotoSet()

    print("Calculating mean month...")
    months = [v.time.month for v in values]
    month_mean = cycle_avg(months, 12)
    print("It is %f, saving..." % month_mean)
    normalized_set.month_mean = month_mean

    print("Calculating mean hour...")
    hours = [v.time.hour for v in values]
    hour_mean = cycle_avg(hours, 24)
    print("It is %f, saving..." % hour_mean)
    normalized_set.hour_mean = hour_mean

    print("Calculating mean x...")
    x = [v.location[0] for v in values]
    x_mean = np.mean(x)
    print("It is %f, saving..." % x_mean)
    normalized_set.location_x_mean = x_mean

    print("Calculating mean y...")
    y = [v.location[1] for v in values]
    y_mean = np.mean(y)
    print("It is %f, saving..." % y_mean)
    normalized_set.location_y_mean = y_mean

    print("Calculating month MAD...")
    def dist12(a, b):
        return cyclical_distance(a,b,12) 
    month_mad = mean_absolute_deviation(months, month_mean, dist12)
    print("It is %f, saving..." % month_mad)
    normalized_set.month_deviation = month_mad

    print("Calculating hour MAD...")
    def dist24(a, b):
        return cyclical_distance(a,b, 24)
    hour_mad = mean_absolute_deviation(hours, hour_mean, dist24)
    print("It is %f, saving..." % hour_mad)
    normalized_set.hour_deviation = hour_mad

    print("Calculating x MAD...")
    x_mad = mean_absolute_deviation(x, x_mean)
    print("It is %f, saving..." % x_mad)
    normalized_set.location_x_deviation = x_mad

    print("Calculating y MAD...")
    y_mad = mean_absolute_deviation(y, y_mean)
    print("It is %f, saving..." % y_mad)
    normalized_set.location_y_deviation = y_mad

    normalized_set.save()
    print("All done")