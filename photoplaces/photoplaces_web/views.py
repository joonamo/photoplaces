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

def standard_data():
    return {
        "FLICKR_API_KEY" : settings.FLICKR_API_KEY,
        "GOOGLE_API_KEY" : settings.GOOGLE_API_KEY
    } 

def index(request):
    data = standard_data()
    return render_to_response('index.html',data,context_instance=RequestContext(request))

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