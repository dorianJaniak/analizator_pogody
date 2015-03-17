'''
Created on Mar 17, 2015

'''

from django.conf.urls import patterns, url
from Analyzer import views

urlpatterns=patterns('',url(r'^$',views.index,name='index'))