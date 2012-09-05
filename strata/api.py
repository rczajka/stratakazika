from django.conf import settings
from django.db.models import Sum
from strata import store
from strata.models import Counter, CounterInc
from strata.search import word_starts_with


def search_counter(prefix):
    if len(prefix) < 1:
        return []
    return Counter.objects.filter(word_starts_with('name', prefix), hidden=False)


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
    store.incr('strata_sum_count', 1)
    store.incr('strata_sum_money', 100*price)
    if log:
        counter.counterinc_set.create(money=price,
                total_count = counter.count, total_money = counter.money)


def last_incs(limit=settings.LAST_INCS):
    return CounterInc.objects.filter(counter__hidden=False).order_by('-date')[:limit]


def popular_counters(limit=settings.POPULAR_COUNTERS):
    return Counter.objects.filter(hidden=False).order_by('-money')[:limit]


def sum_counter():
    sum_count = store.get('strata_sum_count')
    sum_money = store.get('strata_sum_money')
    if sum_count is None or int(sum_count) < 10000 or sum_money is None or int(sum_money) < 10000000:
        summed = Counter.objects.all().aggregate(count=Sum('count'), money=Sum('money'))
        store.set('strata_sum_count', summed['count'])
        store.set('strata_sum_money', int(summed['money'] * 100))
        return summed
    return {'count': int(sum_count), 'money': float(sum_money)/100}
    # return Counter.objects.all().aggregate(count=Sum('count'), money=Sum('money'))


def the_counter():
    counter, created = Counter.objects.get_or_create(name=settings.THE_COUNTER)
    return counter


def inc_the_counter():
    inc_counter(the_counter(), log=False)
