from django import template

register = template.Library()

@register.inclusion_tag("strata/inc_form.html")
def inc_form(counter, prefix=""):
    return locals()
