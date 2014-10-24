# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 22:47:44 2014

@author: kevyuan
"""

import numpy as np
import statsmodels.api as sm
import pylab as pl

##############

year = [1, 2, 3, 4, 5]

sales = [120000, 443243, 1176471, 2587500, 4937500]

# assuming year 5’s GNP = year 5’s (Q1~Q4 GNP)/4 
gnp = [97.3, 98.3, 100.1, 103.2, 105.625]

mkt = [1500000, 1700000, 3200000, 7100000, 18200000]

price = [125, 92.5, 85, 80, 80]


pl.plot(year, sales)
pl.plot(year, gnp)
pl.plot(year, mkt)
pl.plot(year, price)
#pl.show()

print "*********** sales regression *************\n"
x = np.column_stack((price,mkt,gnp))  #stack explanatory variables into an array

xc = sm.add_constant(x, prepend=True) #add a constant

res = sm.OLS(sales,xc).fit() #create a model and fit it
print res.params
print res.bse
print res.summary()


