from __future__ import print_function
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from patsy import dmatrices
import statsmodels.api as sm
import statsmodels.tsa.arima_process as arimap


#dta = pd.read_csv("a.csv")
dta =pd.read_csv("d.csv", parse_dates=True, index_col=[0])
dta.plot(figsize=(12,8));		#Czyste dane
print(len(dta))
nLags = 40

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

acf_acf, acf_confint = sm.tsa.acf(dta.values.squeeze(), nlags=nLags, alpha=0.05)
pacf_pacf, pacf_confint = sm.tsa.pacf(dta.values.squeeze(), nlags=nLags,  alpha=0.05, method = 'ols')
lags = np.arange(nLags+1)
acf_confint = acf_confint - acf_confint.mean(1)[:,None]
pacf_confint = pacf_confint - pacf_confint.mean(1)[:,None]

ax1.plot(lags,acf_acf)
ax1.fill_between(lags,acf_confint[:,0], acf_confint[:,1], alpha=.25)
ax1.set_title("ACF")
ax2.plot(lags,pacf_pacf)
ax2.fill_between(lags,pacf_confint[:,0], pacf_confint[:,1], alpha=.25)
ax2.set_title("PACF")

acf_peaks = abs(acf_acf) - abs(acf_confint[:,0])
ax3.plot(lags,acf_peaks)
ax3.set_title("ACF przeciecie 0")
pacf_peaks = abs(pacf_pacf) - abs(pacf_confint[:,0])
ax4.plot(lags,pacf_peaks)
ax4.set_title("PACF przeciecie 0")
plt.show()

#Ostatecznie wyznaczenie proponowanych parametrow p i q
p = 0
q = 0
while p < len(lags) and acf_peaks[p] > 0:
	p = p+1
while q < len(lags) and pacf_peaks[q] > 0:
	q = q+1

print("WYBRANE PARAMETRY P i Q:",p,q)
if(p>q):
	p = int(p/q)
	q = 1
else:
	q = int(q/p)
	p = 1

print("PRZEKONWERTOWANE PARAMETRY P i Q:",p,q)

#DJ: stosujemy ARIMA, poniewaz nadaja sie do szeregow niestacjonarnych 
#DJ: proces stacjonarny ma stala srednia i odchylenie w czasie
#DJ: model ARIMA sprowadza do postaci stacjonarnej dane

#DJ: ARIMA(p,d,q):
# - p - parametr autoregresji (ile wczesniejszych wartosci ma wplyw na aktualna wartosc)
# - d - stopien roznicowania (aby otrzymac proces stacjonarny)
# - q - stopien MA, sredniej ruchomej (ile zaburzen wczesniejszych brac pod uwage)

#Iteracyjna wersja algorytmu - ostatecznie predykcja jest dosc niedokladna
#p = 1
d = 0
#q = 0
#p_best = 1
d_best = 0
#q_best = 0
AIC_best = 999999
#while d <= p:
#	print("TEST ARIMA: ", p,d,q)
#	try:
#		arima_mod = sm.tsa.ARIMA(dta, (p,d,q)).fit()
#		if AIC_best > arima_mod.aic:
#			d_best = d
#			AIC_best = arima_mod.aic
#	except:
#		print("NIESTACJONARNY")
#	finally:
#		d = d+1
print("ARIMA dopasowanie: ",q,d_best,p)
print("AIC: ", AIC_best)

arima_mod = sm.tsa.ARIMA(dta, (p,d_best,q)).fit()
arma_check = arimap.ArmaProcess(arima_mod.arparams,arima_mod.maparams)
print(arma_check.isstationary())

# na stronie badali jeszcze reszty autokorelacji, czy cos takiego
# prognoza jeszcze nie rozgryziona
# DJ: reszta rowniez powinna byc stacjonarna - jesli dobrze zrozumialem
fig, ax = plt.subplots(figsize=(12, 8))
#od argumentu 30 jest juz predykcja
preds = arima_mod.predict(len(dta)-30,len(dta)+30)
print(preds)

x_prediction = np.arange(len(dta)-31,len(dta)+30,1)
plt.plot(x_prediction,preds)
plt.plot(dta)
plt.show()