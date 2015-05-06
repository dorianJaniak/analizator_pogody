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
	maxVal = 100
	if(p>maxVal or q>maxVal):				#Gdy za duze to dlugo generuje sie prognoza
		if(p>q):				
			p = int(p/q)
			q = 1
		else:
			q = int(q/p)
			p = 1
	if(p>maxVal):					#Gdy mimo wszystko nie udalo sie jakos unormowac tych parametrow
		p = maxVal					
	if(q>maxVal):
		q = maxVal
	print("PRZEKONWERTOWANE PARAMETRY P i Q:",p,q)
	return p,q

#def rozniczkuj(dane):
	#i = 0
	#while( i < len(dane)-1 ):
	#	dane.set_value(i, 1, dane.get_value(i+1,1) - dane.get_value(i,1) )
	

#dta = pd.read_csv("a.csv")
dta =pd.read_csv("d.csv", parse_dates=True, index_col=[0])
dta.plot(figsize=(12,8));		#Czyste dane

dane = dta
d = 0
good_proces = False
while (d<=2 and good_proces == False):			#Dopoki proces nie bedzie stacjonarny
	print("SPRAWDZANE D: ",d)
	if(d>0):
		dane = dane.diff(d).dropna()
	p,q = wyznaczPiQ(dane)
	p,q = minimalizujPiQ(p,q)
	try:
		arma_mod = sm.tsa.ARMA(dane,(p,q)).fit(transparams=False)	#Tutaj musi zostac dopasowany proces ARMA
		arma_check = arimap.ArmaProcess(arma_mod.arparams, arma_mod.maparams)
		stationary = arma_check.isstationary()
		invertible = arma_check.isinvertible()
		if(stationary == False):
			print("NIESTACJONARNY")
	#	if(invertible == False):
	#		print("NIEODWRACALNY")
		good_proces = (stationary)
		if(good_proces == False):
			d = d+1
#			dane = dane.diff().dropna()
	except:
		print("NIESTACJONARNY")
		d = d+1
#		dane = dane.diff().dropna()

print ("WYBRANE D: ", d)
p_best = p
d_best = d
q_best = q
p_tmp = p
q_tmp = q
AIC_best = 999999
while p_tmp>=0:
	while q_tmp>=0 and AIC_best == 999999:
		print("TEST ARIMA: ", p_tmp,d,q_tmp)
		try:
			arima_mod = sm.tsa.ARIMA(dane, (p_tmp,d,q_tmp)).fit(transparams=False)
			if AIC_best > arima_mod.aic:
				p_best = p_tmp
				q_best = q_tmp
				AIC_best = arima_mod.aic
		except:
			print("NIESTACJONARNY lub NIEODWRACALNY")
		finally:
			q_tmp = q_tmp -1
	q_tmp = q
	p_tmp = p_tmp -1
print("ARIMA dopasowanie: ",p_best,d_best,q_best)
print("AIC: ", AIC_best)

#dane = dane.diff(4).dropna()
arima_mod_ost = sm.tsa.ARIMA(dane, (p_best,d_best,q_best)).fit(transparams = False)
#arma_check = arimap.ArmaProcess(arima_mod_ost.arparams,arima_mod_ost.maparams)
#print(arma_check.isstationary())

# na stronie badali jeszcze reszty autokorelacji, czy cos takiego
# prognoza jeszcze nie rozgryziona
# DJ: reszta rowniez powinna byc stacjonarna - jesli dobrze zrozumialem
fig, ax = plt.subplots(figsize=(12, 8))
#od argumentu 30 jest juz predykcja
preds = arima_mod_ost.predict(len(dane)-30,len(dane)+30)
#print(preds)

x_prediction = np.arange(len(dta)-31,len(dta)+30,1)
plt.plot(x_prediction,preds)
plt.plot(dta)
plt.show()
