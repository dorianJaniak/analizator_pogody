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
arima_mod20 = sm.tsa.ARIMA(dta, (2,0,0)).fit() 
# te parametry z glowy, trzeba jakas funkcja chyba je znalezc...
arima_mod30 = sm.tsa.ARIMA(dta, (3,0,0)).fit()

#DJ: ALGORYTM:
#DJ: Jeden z pomyslow (ARMA): P - ile pierwszych peakow na ACF znajduje się poza przedzialem ufnosci
#		    D - ile pierwszych peakow na PACF znajduje sie poza przedzialem ufnosci
#	W takiej sytuacji mamy w naszym przykladzie model ARMA (28,2) lub odpowiednio skalujac (14,1) - jakis gosciu tak robil i byl zadowolony z siebie - ale oczywiscie wtedy nie ma parametru d.
#
#DJ: Inny pomysl - rozniczkowac do czasu az stacjonarny i gdy juz stacjonarmy to zbadac tak jak ARMA
#
#DJ: Jeszcze inny pomysl pomyslowych ludzi - zbadac residua (ale jak ?! na co zwrocic uwage ?! Jak zwykle madrzy ludzie pisza tylko, ze mozna badac residua i opisuja co widza, ale po czym to rozpoznaja to juz wzmianki brak ?! Krew mnie zaleje... przepraszam :( ) 
#DJ: Jakas inna metoda pomyslowych dobromirow - AIC

print("Wartosci parametrow")
print(arima_mod20.params)
print(arima_mod30.params)

#DJ: Kryterium informacyjne AIC i BIC im wyzsze tym lepiej
print("Kryterium informacyjne")
print(arima_mod20.aic, arima_mod20.bic, arima_mod20.hqic)
print(arima_mod30.aic, arima_mod30.bic, arima_mod30.hqic)
#DJ: A WIEC - jesli puscic w petli liczenie ARIMA dla roznych parametrow i sprawdzac czy AIC i BIC jest relatywnie wieksze niz w innych kombinacjach parametrow (P,D,Q) to dobierzemy parametry

# na stronie badali jeszcze reszty autokorelacji, czy cos takiego
# prognoza jeszcze nie rozgryziona
# DJ: reszta rowniez powinna byc stacjonarna - jesli dobrze zrozumialem
fig, ax = plt.subplots(figsize=(12, 8))
ax = dta.ix[200:].plot(ax=ax)
preds = arima_mod30.predict(220,340)
#fig = arima_mod30.plot_predict(220, 340, dynamic=True, plot_insample=False)
print(preds)
plt.show()
