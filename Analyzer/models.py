# -*- coding: utf-8 -*-
from __future__ import print_function
#from adaptor.model import CsvModel
from django.shortcuts import  get_object_or_404

import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from patsy import dmatrices
import statsmodels.api as sm
import statsmodels.tsa.arima_process as arimap
#from django.pandas.io import read_frame
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
# prognoza

from django_pandas.io import read_frame
from django_pandas.managers import DataFrameManager

from django.db import models
from datetime import datetime



# Create your models here.

class Stacja(models.Model):
    # id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=30)

    def __str__(self):
        return self.nazwa

class Jednostka(models.Model):
    # id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=20)

    def __str__(self):
        return self.nazwa

class RodzajPomiaru(models.Model):
    # id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=20)
    jednostka = models.ForeignKey(Jednostka,null=True)

    def __str__(self):
        return self.nazwa


class DanePomiarowe(models.Model):
    # id = models.AutoField(primary_key=True)
    wartosc = models.IntegerField()
    rodzaj_pomiaru = models.ForeignKey(RodzajPomiaru, null=True)
    stacja = models.ForeignKey(Stacja, null=True)
    data = models.DateTimeField(default=datetime.now(), null=True)

    objects = DataFrameManager()

    def __str__(self):
        return "%s [%s] @ %s" % (self.wartosc, self.rodzaj_pomiaru, self.stacja)

# class DanePomiaroweCsvModel(CsvModel):
#     wartosc = IntegerField()
#     rodzaj_pomiaru = DjangoModelField(RodzajPomiaru)
#     stacja = DjangoModelField(RodzajPomiaru)
#     data = DateField()
#
#     class Meta:
#         delimiter= ","
#         dbModel=DanePomiarowe
#


class Algorithm:
    #To jest bardzo artystyczna prognoza pogody
    def __init__(self, dlugosc_prognozy, stacja_id, rodzaj_pomiaru):
        self.ileDniPrognoza = dlugosc_prognozy
        stacja_q=get_object_or_404(Stacja,id=stacja_id)
        rodzaj_pomiaru_q=get_object_or_404(RodzajPomiaru,id=rodzaj_pomiaru
                                           )
        qs = DanePomiarowe.objects.filter(stacja=stacja_q, rodzaj_pomiaru=rodzaj_pomiaru_q)
        self.dta=qs.to_dataframe(
            fieldnames=['data','wartosc'],
            index='data'
        )
        # self.dta=qs.to_timeseries(
        #     fieldnames=['data','wartosc'],
        #     index='data',
        #     #pivot_columns='wartosc',
        #     values='wartosc',
        #     storage='wide'
        # )
        print(self.dta)
        print(len(self.dta))

        self.preds=[]
        self.x_prediction=[]



    def wyznaczPiQ(self,dane):
        nLags = 40
        acf_acf, acf_confint = sm.tsa.acf(dane, nlags=nLags, alpha=0.05)
        pacf_pacf, pacf_confint = sm.tsa.pacf(dane, nlags=nLags,  alpha=0.05, method = 'ols')
        lags = np.arange(nLags+1)
        acf_confint = acf_confint - acf_confint.mean(1)[:,None]
        pacf_confint = pacf_confint - pacf_confint.mean(1)[:,None]

        #fig = plt.figure(figsize=(12,8))
        #ax1 = fig.add_subplot(211)
        #ax2 = fig.add_subplot(212)

        #ax1.plot(lags,acf_acf)
        #ax1.fill_between(lags,acf_confint[:,0], acf_confint[:,1], alpha=.25)
        #ax1.set_title("ACF")
        #ax2.plot(lags,pacf_pacf)
        #ax2.fill_between(lags,pacf_confint[:,0], pacf_confint[:,1], alpha=.25)
        #ax2.set_title("PACF")

        acf_peaks = abs(acf_acf) - abs(acf_confint[:,0])
        pacf_peaks = abs(pacf_pacf) - abs(pacf_confint[:,0])

        #Ostatecznie wyznaczenie proponowanych parametrow p i q
        p = 0
        q = 0
        while p < len(lags) and pacf_peaks[p] > 0:
            p = p+1
        while q < len(lags) and acf_peaks[q] > 0:
            q = q+1
        #print("WYBRANE PARAMETRY P i Q:",p,q)
        #plt.show()
        return p,q

    def minimalizujPiQ(self,p,q):
        maxVal = 20
        if(p>maxVal or q>maxVal):
            if(p>q):
                p = int(p/q)
                q = 1
            else:
                q = int(q/p)
                p = 1
        if(p>maxVal):
            p = maxVal
        if(q>maxVal):
            q = maxVal
        #print("PRZEKONWERTOWANE PARAMETRY P i Q:",p,q)
        return p,q

    def artistico_usrednijWykres(self, dane,rzad,ileNowych):
        #print(" w funckji")
        daneX = range(0,len(dane.values.squeeze()))
        coef = np.polyfit(daneX,dane.values.squeeze(),rzad)
        polynomial = np.poly1d(coef)
        ys = polynomial(range(0,len(dane.values.squeeze())+ileNowych))
        return ys

    def artistico_odejmijTrend(self,daneOryg,trend):
        wynik = daneOryg.values.squeeze()
        for i in range(0,len(daneOryg.values.squeeze() )):
            wynik[i] = wynik[i] - trend[i]
        return wynik

    def artistico_obliczWzmocnienie(self,dane,predykcja,trend,ileBracPodUwage):
        kPredykcja = predykcja.copy().values.squeeze()
        if(ileBracPodUwage>10):
            ileBracPodUwage = 10
        sredniaPred = 0
        maxPred = -9999999
        minPred = 9999999
        for i in range(30,30+ileBracPodUwage):
            sredniaPred = sredniaPred + kPredykcja[i]
            if kPredykcja[i]<minPred:
                minPred = kPredykcja[i]
            if kPredykcja[i]>maxPred:
                maxPred = kPredykcja[i]
        sredniaPred = sredniaPred / ileBracPodUwage
        sredniaDane = 0
        maxDane = -9999999
        minDane = 9999999
        kDane = dane.values.squeeze()
        for i in range(len(kDane)-ileBracPodUwage,len(kDane)):
            sredniaDane = sredniaDane + kDane[i]
            if kDane[i]<minDane:
                minDane = kDane[i]
            if kDane[i]>maxDane:
                maxDane = kDane[i]
        sredniaDane = sredniaDane / ileBracPodUwage

        wspWGore = (maxDane-sredniaDane)/(maxPred-sredniaPred)
        wspWDol = (minDane-sredniaDane)/(minPred-sredniaPred)

        #print("WZMOCNIENIE:",wspWGore, wspWDol)

        kPredykcja = predykcja.values.squeeze()
        for i in range(30,len(kPredykcja)):
            if kPredykcja[i] > sredniaPred:
    #			kPredykcja[i] = (kPredykcja[i]-sredniaPred)*wspWGore + sredniaPred;
                kPredykcja[i] = (kPredykcja[i]-sredniaPred)*wspWGore + trend[i-1];
                #print(kPredykcja[i],trend[i-1],i)
            else:
    #			kPredykcja[i] = sredniaPred - ((sredniaPred-kPredykcja[i])*wspWDol);
                kPredykcja[i] = trend[i-1] - ((sredniaPred-kPredykcja[i])*wspWDol)
                #print(kPredykcja[i],trend[i-1],i)
        return 0


    def mainAlg(self):

        # ileDniPrognoza = 14
        #dta =pd.read_csv("d.csv", parse_dates=True, index_col=[0])

        #fig = Figure()
        #ax1 = fig.add_subplot(211)
        #ax2 = fig.add_subplot(212)
        # dta.plot(figsize=(12,8));
        self.artistico_trend = self.artistico_usrednijWykres(dane=self.dta.copy(),rzad=20,ileNowych=self.ileDniPrognoza)
        self.artistico_wahania = self.artistico_odejmijTrend(daneOryg=self.dta.copy(),trend=self.artistico_trend)


        # fig = plt.figure(figsize=(12,8))
        # ax1 = fig.add_subplot(211)
        # ax2 = fig.add_subplot(212)
        # ax1.plot(dta)
        # ax1.plot(artistico_trend)
        # ax2.plot(artistico_wahania)
        # plt.show()

        #gdyby tutaj zrobic bez dta.copy to zmiany zostana zatwierdzone

        good_proces = False
        p,q = self.wyznaczPiQ(dane=self.dta)
        #print("tutej 1.5")

        p,q = self.minimalizujPiQ(p,q)
        #print("tutej 2")


        p_best = p
        q_best = q
        p_tmp = p
        q_tmp = q
        AIC_best = 99999999
        while p_tmp>=1:
            while q_tmp>=0:
                # print("TEST ARMA: ", p_tmp,q_tmp)
                try:
                    arma_mod = sm.tsa.ARMA(self.dta, (p_tmp,q_tmp)).fit()
                    if AIC_best > arma_mod.aic:
                        p_best = p_tmp
                        q_best = q_tmp
                        AIC_best = arma_mod.aic
                except:
                    pass
                    # print("NIESTACJONARNY lub NIEODWRACALNY")
                finally:
                    q_tmp = q_tmp -1
            q_tmp = q
            p_tmp = p_tmp -1
        #print("ARMA dopasowanie: ",p_best,q_best)
        #print("AIC: ", AIC_best)

        arma_mod = sm.tsa.ARMA(self.dta, (p_best,q_best)).fit()
        arma_check = arimap.ArmaProcess(arma_mod.arparams,arma_mod.maparams)
        # print(arma_check.isstationary())

        # fig, ax = plt.subplots(figsize=(12, 8))
        self.preds = arma_mod.predict(len(self.dta)-30,len(self.dta)+self.ileDniPrognoza)

        self.x_prediction = np.arange(len(self.dta)-31,len(self.dta)+self.ileDniPrognoza,1)
        self.artistico_obliczWzmocnienie(self.dta,self.preds,self.artistico_trend[len(self.dta)-30:],self.ileDniPrognoza)
        # plt.plot(x_prediction,self.preds)
        # plt.plot(dta)
        # plt.show()
        print(" PROCESSING DONE ")

        # print("PREDYKCJA:", self.preds[30:])