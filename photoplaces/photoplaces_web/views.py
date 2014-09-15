from django.shortcuts import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.forms.models import modelform_factory
from django.contrib import auth
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm

import location_query_json

def index(request):
    return render_to_response('index.html',context_instance=RequestContext(request))

# Create your views here.
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