from __future__ import print_function
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from patsy import dmatrices
import statsmodels.api as sm

#dta = pd.read_csv("a.csv")
dta =pd.read_csv("d.csv", parse_dates=True, index_col=[0])
dta.plot(figsize=(12,8));

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(dta.values.squeeze(), lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(dta, lags=40, ax=ax2)


arima_mod20 = sm.tsa.ARIMA(dta, (2,0,0)).fit() 
# te parametry z glowy, trzeba jakas funkcja chyba je znalezc...
arima_mod30 = sm.tsa.ARIMA(dta, (3,0,0)).fit()

print("Wartosci parametrow")
print(arima_mod20.params)
print(arima_mod30.params)

print("Kryterium informacyjne")
print(arima_mod20.aic, arima_mod20.bic, arima_mod20.hqic)
print(arima_mod30.aic, arima_mod30.bic, arima_mod30.hqic)

# na stronie badali jeszcze reszty autokorelacji, czy cos takiego
# prognoza jeszcze nie rozgryziona
fig, ax = plt.subplots(figsize=(12, 8))
ax = dta.ix[200:].plot(ax=ax)
fig = arima_mod30.plot_predict(220, 340, dynamic=True, plot_insample=False)

plt.show()
