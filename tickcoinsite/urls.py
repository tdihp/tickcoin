from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'tickcoin.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'tickcoin.views.logout'),
    # url(r'^done/$', 'example.app.views.done', name='done'),

    url(r'', include('social.apps.django_app.urls', namespace='social')),

    url(r'^slots/(?P<slot_name>\w+)/counters/(?P<counter_name>\w+)$', 'tickcoin.views.counter'),
    url(r'^slots/(?P<slot_name>\w+)/ticks$', 'tickcoin.views.tick'),
    url(r'^slots$', 'tickcoin.views.slots'),
)
