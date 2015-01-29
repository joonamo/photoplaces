from django.shortcuts import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.forms.models import modelform_factory
from django.contrib import auth
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
import location_query_json
from models import PhotoLocationEntry, PhotoCluster, PhotoClusterRun
from pprint import pprint
from random import randrange, shuffle

def standard_data():
    return {
        "FLICKR_API_KEY" : settings.FLICKR_API_KEY,
        "GOOGLE_API_KEY" : settings.GOOGLE_API_KEY
    } 

def index(request):
    data = standard_data()

    cluster_runs = []
    for run in PhotoClusterRun.objects.all():
        run_info = {
            "id": run.id,
            "comment": run.comment,
            "algorithm": run.get_algorithm_display()
        }
        cluster_runs.append(run_info)
    data["cluster_runs"] = cluster_runs

    return render_to_response('index.html', data, context_instance=RequestContext(request))

def photos_box_contains(request):
    q = request.GET
    x0 = q["x0"]
    y0 = q["y0"]
    x1 = q["x1"]
    y1 = q["y1"]
    srid = None
    if "srid" in q:
        srid = q["srid"]

    return HttpResponse(location_query_json.photos_box_contains(x0, y0, x1, y1, srid))

def clusters_box_contains(request):
    q = request.GET
    x0 = q["x0"]
    y0 = q["y0"]
    x1 = q["x1"]
    y1 = q["y1"]
    srid = None
    if "srid" in q:
        srid = q["srid"]

    return HttpResponse(location_query_json.clusters_box_contains(x0, y0, x1, y1, srid = srid))

def clustering_run_get(request):
    q = request.GET
    pk = q["id"]

    return HttpResponse(location_query_json.clustering_run_get(pk))

def cluster_get(request):
    q = request.GET
    pk = q["id"]

    return HttpResponse(location_query_json.cluster_get(pk))

def cluster_get_stats(request):
    q = request.GET
    pk = q["id"]

    return HttpResponse(location_query_json.cluster_get_stats(pk))

def sidebar_photos_ajax(request):
    if not request.is_ajax():
        raise PermissionDenied
    q = request.GET
    pk = q["id"]
    data = standard_data()

    cluster = PhotoCluster.objects.get(pk = pk)
    pks = list(cluster.photos.all().values_list("id", flat=True))
    shuffle(pks)
    photos = []
    for point in PhotoLocationEntry.objects.filter(id__in = pks[:30]).values("photo_url", "photo_id", "time", "photo_title"):
        photos.append(point)
    data["photos"] = photos

    return render_to_response('sidebar_photos_ajax.html', data, context_instance=RequestContext(request))