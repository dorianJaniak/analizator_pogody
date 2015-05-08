# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, \
    render_to_response
from Analyzer.models import Jednostka, RodzajPomiaru,DanePomiarowe, \
    Stacja, Algorithm
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView,\
    UpdateView, DeleteView
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
from matplotlib import pylab
import random
import datetime


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
        print(context['station'])
        context['dane_pom'] = DanePomiarowe.objects.filter(stacja__id=station_id)
        return context

class ForecastView(TemplateView):
    template_name = "analyzer/forecast.html"

class AuthorsView(TemplateView):
    template_name='analyzer/authors.html'

# TODO
def dataview(request):
    pass
    alg = Algorithm(dlugosc_prognozy=14)

    fig=Figure()
    ax=fig.add_subplot(111)
    ax.plot(alg.dta)
    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
    # alg = Algorithm(dlugosc_prognozy=14)
    # fig =  plt.figure(1,figsize=(12,8))
    # plt.plot(alg.dta)
    # canvas=FigureCanvas(fig)
    # response=HttpResponse(content_type='image/png')
    # canvas.print_png(response)
    # plt.close(fig)
    # return response

    #


    # alg = Algorithm(dlugosc_prognozy=14)
    # alg.mainAlg()
    #
    # fig, ax = plt.subplots(figsize=(12, 8))
    # plt.plot(alg.x_prediction,alg.preds)
    # plt.plot(alg.dta)
    #
    # #fig = Figure()
    # #ax1 = fig.add_subplot(211)
    # #ax2 = fig.add_subplot(212)
    #
    # canvas=FigureCanvas(fig)
    # response=HttpResponse(content_type='image/png')
    # canvas.print_png(response)
    # plt.close(fig)
    # return response
