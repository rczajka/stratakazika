# -*- coding: utf-8 -*-
import json
import re
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_POST
from pluralize_pl.templatetags.pluralize_pl import pluralize_pl
from strata import store
from strata import api
from strata import tasks
from strata.templatetags.strata_tags import money


@cache_control(max_age=10)
def home(request):
    return render(request, "strata/home.html", {
            "DEFAULT_PRICE": settings.DEFAULT_PRICE,
            "last_incs": api.last_incs(),
            "popular_counters": api.popular_counters(),
            "the_counter": api.the_counter(),
            "sum_counter": api.sum_counter(),
            "linked": api.counter_by_name(request.GET.get('i')),
        })


@cache_control(max_age=60)
def hint(request):
    result = [counter.name 
        for counter in api.search_counter(request.GET.get('term', ''))[:10]]
    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_POST
def increase(request):
    name = request.POST.get('counter_name')
    name = re.sub(ur"\s+", " ", name.strip())

    # Flood control.
    ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
    key = ('inc', ip, name)
    if store.get(key):
        return HttpResponseForbidden(u'Flood')
    store.set(key, 1)
    store.expire(key, 3)

    if name:
        #tasks.inc_counter_by_name.delay(name)
        api.inc_counter_by_name(name)
    if request.is_ajax():
        return  HttpResponse('') #update(request)
    else:
        return  redirect('/')


@cache_control(max_age=10)
def update(request):
    sum_counter = api.sum_counter()
    result = {
        "the_count": u"(%s %s)" % (
                intcomma(sum_counter['count']),
                pluralize_pl(sum_counter['count'], u"kopia,kopii,kopie")
            ),
        "the_money": money(sum_counter['money']),
    }
    return HttpResponse(json.dumps(result), mimetype="application/json")
