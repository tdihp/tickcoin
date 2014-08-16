import json

from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login
from django.views.decorators.http import require_http_methods

from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.backends.google import GooglePlusAuth
from social.backends.utils import load_backends



def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


@login_required
def home(request):
    return render(request, 'index.html')


def slots(request):
    available_counters = [
        {'counter_name': 'total', 'text': 'Total'},
        {'counter_name': 'day', 'text': 'Day'},
        {'counter_name': 'week', 'text': 'Week'},
        {'counter_name': 'month', 'text': 'Month'},
        {'counter_name': 'year', 'text': 'Year'},
    ]
    jdata = {
        'slots': [
            {'name': "sky", 'available_counters': available_counters},
            {'name': "vine", 'available_counters': available_counters},
            {'name': "lava", 'available_counters': available_counters},
        ]
    }
    data = json.dumps(jdata)
    print data
    return HttpResponse(data, content_type="application/json")



def counter(request, slot_name,  counter_name):
    import random
    g_counter = random.randint(0, 100)
    jdata = {'ticks': g_counter}
    return HttpResponse(json.dumps(jdata), content_type="application/json")


@require_http_methods(["GET", "POST"])
def tick(request, slot_name):
    return HttpResponse(json.dumps({'result': 'OK'}), content_type="application/json")
