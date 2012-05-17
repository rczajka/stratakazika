from django.conf import settings
from django.db.models import Sum
from strata.models import Counter, CounterInc
from strata.search import word_starts_with


def search_counter(prefix):
    # Prefix must have at least 2 characters
    if len(prefix) < 1:
        return []
    return Counter.objects.filter(word_starts_with('name', prefix))


def counter_by_name(name):
    try:
        return Counter.objects.get(name=name)
    except Counter.DoesNotExist:
        return None


def inc_counter_by_name(name):
    counter, created = Counter.objects.get_or_create(name=name)
    inc_counter(counter)


def inc_counter(counter, log=True):
    counter.count += 1
    price = counter.price if counter.price else settings.DEFAULT_PRICE
    counter.money += price
    counter.save()
    if log:
        counter.counterinc_set.create(money=price)


def last_incs(limit=settings.LAST_INCS):
    return CounterInc.objects.all().order_by('-date')[:limit]


def popular_counters(limit=settings.POPULAR_COUNTERS):
    return Counter.objects.all().order_by('-money')[:limit]


def sum_counter():
    return Counter.objects.all().aggregate(count=Sum('count'), money=Sum('money'))


def the_counter():
    counter, created = Counter.objects.get_or_create(name=settings.THE_COUNTER)
    return counter


def inc_the_counter():
    inc_counter(the_counter(), log=False)
