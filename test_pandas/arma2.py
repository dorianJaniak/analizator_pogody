from __future__ import print_function
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from patsy import dmatrices
import statsmodels.api as sm

#dta = pd.read_csv("a.csv")
dta =pd.read_csv("d.csv", parse_dates=True, index_col=[0])
dta.plot(figsize=(12,8));		#Czyste dane
print(len(dta))

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(dta.values.squeeze(), lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(dta, lags=40, ax=ax2)

#DJ: stosujemy ARIMA, poniewaz nadaja sie do szeregow niestacjonarnych 
#DJ: proces stacjonarny ma stala srednia i odchylenie w czasie
#DJ: model ARIMA sprowadza do postaci stacjonarnej dane

#DJ: ARIMA(p,d,q):
# - p - parametr autoregresji (ile wczesniejszych wartosci ma wplyw na aktualna wartosc)
# - d - stopien roznicowania (aby otrzymac proces stacjonarny)
# - q - stopien MA, sredniej ruchomej (ile zaburzen wczesniejszych brac pod uwage)


p = 1
d = 0
q = 0
p_best = 1
d_best = 0
q_best = 0
AIC_best = 999999
#while p < 4:
#	while q<=p:
#		while d <= p:
#			print("TEST ARIMA: ", p,d,q)
#			try:
#				arima_mod = sm.tsa.ARIMA(dta, (p,d,q)).fit()
#				if AIC_best > arima_mod.aic:
#					p_best = p
#					d_best = d
#					q_best = q
#					AIC_best = arima_mod.aic
#			except:
#				print("NIESTACJONARNY")
#			finally:
#				d = d+1
#		q=q+1
#		d=0
#	p=p+1
#	q=0

print("ARIMA dopasowanie: ",p_best,d_best,q_best)
print("AIC: ", AIC_best)
arima_mod = sm.tsa.ARIMA(dta, (p,d,q)).fit()
arima_mod = sm.tsa.ARIMA(dta, (14,0,2)).fit()
#gdy w wyniku otrzyma sie nie stacjonarny proces to rzuca wyjatkiem

#print("Wartosci parametrow")
#print(arima_mod.params)

#DJ: Kryterium informacyjne AIC i BIC im NIZSZE tym lepiej
#print("Kryterium informacyjne")
#print(arima_mod.aic, arima_mod.bic, arima_mod.hqic)

# na stronie badali jeszcze reszty autokorelacji, czy cos takiego
# prognoza jeszcze nie rozgryziona
# DJ: reszta rowniez powinna byc stacjonarna - jesli dobrze zrozumialem
fig, ax = plt.subplots(figsize=(12, 8))
#ax = dta.ix[200:].plot(ax=ax)
#od 30 punktu jest juz predykcja
preds = arima_mod.predict(len(dta)-30,len(dta)+30)
#fig = arima_mod.plot_predict(220, 340, dynamic=True, plot_insample=False)
print(preds)
plt.plot(preds)
#preds.plot(figsize=(12,8))
plt.show()
