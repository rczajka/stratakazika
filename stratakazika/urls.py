from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'strata.views.home', name='home'),
    url(r'^podbij$', 'strata.views.increase', name='strata_increase'),
    url(r'^hint$', 'strata.views.hint', name='strata_hint'),
    url(r'^fetch$', 'strata.views.update', name='strata_update'),

    url(r'kopiowanie-to-kradziez/?', RedirectView.as_view(url='/')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
