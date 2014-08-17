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

from .models import Slot, Tick


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


@login_required
def home(request):
    return render(request, 'index.html')


@login_required
def slots(request):
    user = request.user

    available_counters = [
        {'counter_name': 'total', 'text': 'Total'},
        {'counter_name': 'day', 'text': 'Day'},
        {'counter_name': 'week', 'text': 'Week'},
        {'counter_name': 'month', 'text': 'Month'},
        {'counter_name': 'year', 'text': 'Year'},
    ]
    slots = list({'name': slot.name, 'available_counters': available_counters} \
                 for slot in Slot.objects.filter(user=user).order_by('pk'))
    jdata = {'slots': slots}
    data = json.dumps(jdata)
    return HttpResponse(data, content_type="application/json")


@login_required
def counter(request, slot_name, counter_name):
    user = request.user
    slot = Slot.objects.get(user=user, name=slot_name)
    cnt = Tick.objects.filter(slot=slot).count()
    jdata = {'ticks': cnt}
    return HttpResponse(json.dumps(jdata), content_type="application/json")


@require_http_methods(["POST"])
def tick(request, slot_name):
    user = request.user
    slot = Slot.objects.get(user=user, name=slot_name)
    new_tick = Tick.objects.create(slot=slot)
    new_tick.save()
    return HttpResponse(json.dumps({'result': 'OK'}), content_type="application/json")
