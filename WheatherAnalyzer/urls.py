from django.conf.urls import patterns, include, url
from django.contrib import admin
from Analyzer.views import IndexView, StationsView, \
    StationsDetailView, ForecastView, AuthorsView, \
    dataview, data_station_view, \
    LoginView, LogoutView, LoadDataView

# urlpatterns=patterns('',url(r'^$',views.index,name='index'))
urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^station/$', StationsView.as_view(), name="stations"),
    url(r'^station/(?P<station_id>[0-9]+)$', StationsDetailView.as_view(), name="station_detail"),
    url(r'^forecast/$', ForecastView.as_view(), name="forecast"),
    url(r'^authors/$',AuthorsView.as_view(),name='authors'),
    url(r'^forecast/forecast.png$',dataview,name='image_forecast'),
    url(r'^station/(?P<station_id>[0-9]+)/current.png$',data_station_view,name='image_current'),
    url(r'^load_data/$', LoadDataView.as_view() , name="load_data"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^admin/', include(admin.site.urls)),
]