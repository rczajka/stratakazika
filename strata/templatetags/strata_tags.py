from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.inclusion_tag("strata/inc_form.html")
def inc_form(counter, prefix=""):
    return locals()


@register.filter
def money(value):
    return "%s PLN" % intcomma(value)
