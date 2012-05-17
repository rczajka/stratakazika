from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.inclusion_tag("strata/inc_form.html")
def inc_form(counter, prefix=""):
    return locals()


@register.filter
def money(value):
    return "%s PLN" % intcomma(str(value), use_l10n=False).replace(',', ' ').replace('.', ',')


@register.inclusion_tag("strata/counter_item.html")
def counter_item(counter):
    return {
        "counter": counter,
        "money": counter.money,
        "count": counter.count,
    }

@register.inclusion_tag("strata/counter_item.html")
def counterinc_item(inc):
    return {
        "inc": inc,
        "counter": inc.counter,
        "money": inc.total_money,
        "count": inc.total_count,
    }
