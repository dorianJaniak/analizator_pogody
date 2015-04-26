from django.shortcuts import render, get_object_or_404, \
    render_to_response
from Analyzer.models import Jednostka, RodzajPomiaru,DanePomiarowe, \
    Stacja
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView,\
    UpdateView, DeleteView
from django.http import HttpResponse

# Create your views here.

class IndexView(TemplateView):
    template_name = "analyzer/index.html"



class StationsView(TemplateView):
    template_name = "analyzer/stations.html"

    def get_context_data(self, **kwargs):
        context = super(StationsView, self).get_context_data(**kwargs)
        context['station_list'] = Stacja.objects.all()
        return context

class StationsDetailView(TemplateView):
    template_name = "analyzer/stations_detail.html"

    def get_context_data(self, **kwargs):
        station_id = kwargs['station_id']
        context = super(StationsDetailView, self).get_context_data(**kwargs)
        context['station'] = get_object_or_404(Stacja, id=station_id)
        context['dane_pom'] = DanePomiarowe.objects.filter(stacja__id=station_id)
        return context

class ForecastView(TemplateView):
    template_name = "analyzer/forecast.html"

class AuthorsView(TemplateView):
    template_name='analyzer/authors.html'
