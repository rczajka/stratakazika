from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from strata import api


def home(request):
    return render(request, "strata/home.html", {
            "last_incs": api.last_incs(),
            "popular_counters": api.popular_counters(),
            "the_counter": api.the_counter(),
            "sum_counter": api.sum_counter(),
            "linked": api.counter_by_name(request.GET.get('i')),
        })



@require_POST
def increase(request):
    name = request.POST.get('counter_name')
    if name:
        api.inc_counter_by_name(name)
    return redirect('/')
