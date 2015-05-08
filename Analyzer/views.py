# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, \
    render_to_response
from Analyzer.models import Jednostka, RodzajPomiaru,DanePomiarowe, \
    Stacja, Algorithm
from Analyzer.forms import LoginForm
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
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required(redirect_field_name=reverse_lazy('index'), login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class PermissionRequiredMixin(object):
    permission_required = ()

    @method_decorator(login_required(redirect_field_name=reverse_lazy('index'), login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission_required):
            return super(PermissionRequiredMixin, self).dispatch(
                request, *args, **kwargs)
        else:
            return render(request, 'analyzer/403.html', status=403)

class IndexView(TemplateView):
    template_name = "analyzer/index.html"

class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    template_name = "analyzer/login.html"
    success_url = reverse_lazy('index')
    form_class = LoginForm
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.REQUEST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to

class LogoutView(TemplateView):
    template_name = "analyzer/logout.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


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

class AuthorsView(LoginRequiredMixin,TemplateView):
    template_name='analyzer/authors.html'

# TODO
def dataview(request, *args, **kwargs ):
    pass
    alg = Algorithm(dlugosc_prognozy=14)
    alg.mainAlg()

    fig=Figure()
    ax=fig.add_subplot(111)
    #ax.plot(alg.dta)
    ax.plot(alg.x_prediction,alg.preds)
    ax.plot(alg.dta)
    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

def data_station_view(request, *args, **kwargs ):
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
