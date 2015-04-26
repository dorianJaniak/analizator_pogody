from django.conf.urls import patterns, include, url
from django.contrib import admin
from Analyzer.views import IndexView, StationsView, \
    StationsDetailView, ForecastView, AuthorsView

# urlpatterns=patterns('',url(r'^$',views.index,name='index'))
urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^station/$', StationsView.as_view(), name="stations"),
    url(r'^station/(?P<station_id>[0-9]+)$', StationsDetailView.as_view(), name="station_detail"),
    url(r'^forecast/$', ForecastView.as_view(), name="forecast"),
    url(r'^authors/$',AuthorsView.as_view(),name='authors'),
    url(r'^admin/', include(admin.site.urls)),
]