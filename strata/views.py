# -*- coding: utf-8 -*-
import json
import re
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from pluralize_pl.templatetags.pluralize_pl import pluralize_pl
from strata import api
from strata.templatetags.strata_tags import money


def home(request):
    return render(request, "strata/home.html", {
            "last_incs": api.last_incs(),
            "popular_counters": api.popular_counters(),
            "the_counter": api.the_counter(),
            "sum_counter": api.sum_counter(),
            "linked": api.counter_by_name(request.GET.get('i')),
        })


def hint(request):
    result = [counter.name 
        for counter in api.search_counter(request.GET.get('term', ''))[:10]]
    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_POST
def increase(request):
    name = request.POST.get('counter_name')
    name = re.sub(ur"\s+", " ", name.strip())
    if name:
        api.inc_counter_by_name(name)
    if request.is_ajax():
        return  update(request)
    else:
        return  redirect('/')


def update(request):
    sum_counter = api.sum_counter()
    result = {
        "the_count": u"(%d %s)" % (
                sum_counter['count'],
                pluralize_pl(sum_counter['count'], u"kopię,kopii,kopie")
            ),
        "the_money": money(sum_counter['money']),
    }
    return HttpResponse(json.dumps(result), mimetype="application/json")
