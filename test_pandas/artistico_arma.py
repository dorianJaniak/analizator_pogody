#To jest bardzo artystyczna prognoza pogody

from __future__ import print_function
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from patsy import dmatrices
import statsmodels.api as sm
import statsmodels.tsa.arima_process as arimap

def wyznaczPiQ(dane):
	nLags = 40
	acf_acf, acf_confint = sm.tsa.acf(dane, nlags=nLags, alpha=0.05)
	pacf_pacf, pacf_confint = sm.tsa.pacf(dane, nlags=nLags,  alpha=0.05, method = 'ols')
	lags = np.arange(nLags+1)
	acf_confint = acf_confint - acf_confint.mean(1)[:,None]
	pacf_confint = pacf_confint - pacf_confint.mean(1)[:,None]

	fig = plt.figure(figsize=(12,8))
	ax1 = fig.add_subplot(211)
	ax2 = fig.add_subplot(212)

	ax1.plot(lags,acf_acf)
	ax1.fill_between(lags,acf_confint[:,0], acf_confint[:,1], alpha=.25)
	ax1.set_title("ACF")
	ax2.plot(lags,pacf_pacf)
	ax2.fill_between(lags,pacf_confint[:,0], pacf_confint[:,1], alpha=.25)
	ax2.set_title("PACF")

	acf_peaks = abs(acf_acf) - abs(acf_confint[:,0])
	pacf_peaks = abs(pacf_pacf) - abs(pacf_confint[:,0])

	#Ostatecznie wyznaczenie proponowanych parametrow p i q
	p = 0
	q = 0
	while p < len(lags) and pacf_peaks[p] > 0:
		p = p+1
	while q < len(lags) and acf_peaks[q] > 0:
		q = q+1
	print("WYBRANE PARAMETRY P i Q:",p,q)
	#plt.show()
	return p,q

def minimalizujPiQ(p,q):
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
	print("PRZEKONWERTOWANE PARAMETRY P i Q:",p,q)
	return p,q	

def usrednijWykres2(dane,rzad,ileNowych):
	dane2 = range(0,len(dane.values.squeeze()));
	
	coef = np.polyfit(dane2,dane.values.squeeze(),rzad)
	polynomial = np.poly1d(coef)
	ys = polynomial(range(0,len(dane.values.squeeze())+ileNowych))
	return ys



dta =pd.read_csv("d.csv", parse_dates=True, index_col=[0])
dta.plot(figsize=(12,8));

artistico_trend = usrednijWykres2(dta,20,7)
plt.plot(dta)
plt.plot(artistico_trend)
plt.show()

good_proces = False
p,q = wyznaczPiQ(dta)
p,q = minimalizujPiQ(p,q)
	



p_best = p
q_best = q
p_tmp = p
q_tmp = q
AIC_best = 99999999
while p_tmp>=1:
	while q_tmp>=0:
		print("TEST ARMA: ", p_tmp,q_tmp)
		try:
			arma_mod = sm.tsa.ARMA(dta, (p_tmp,q_tmp)).fit()
			if AIC_best > arma_mod.aic:
				p_best = p_tmp
				q_best = q_tmp
				AIC_best = arma_mod.aic
		except:
			print("NIESTACJONARNY lub NIEODWRACALNY")
		finally:
			q_tmp = q_tmp -1
	q_tmp = q
	p_tmp = p_tmp -1
print("ARMA dopasowanie: ",p_best,q_best)
print("AIC: ", AIC_best)

arma_mod = sm.tsa.ARMA(dta, (p_best,q_best)).fit()
arma_check = arimap.ArmaProcess(arma_mod.arparams,arma_mod.maparams)
print(arma_check.isstationary())

fig, ax = plt.subplots(figsize=(12, 8))
preds = arma_mod.predict(len(dta)-30,len(dta)+30)

x_prediction = np.arange(len(dta)-31,len(dta)+30,1)
plt.plot(x_prediction,preds)
plt.plot(dta)
plt.show()
