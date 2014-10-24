# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 22:47:44 2014

@author: kevyuan
"""

import numpy as np
import statsmodels.api as sm
import pylab as pl
import sys

##############

######## calculate index of production ######## 

p = int(input("production (k units):"))

if (p >= 50) and (p < 100):
    pr = np.round(p/10)*10
elif (p >= 100) and (p <= 200):
    pr = np.round(p/20)*20
else:
    print "error, out of scope"
    sys.exit(1) 

print "pr", pr
p_dict = [50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200]
for pi in range(len(p_dict)):
    print "pi", pi
    if p_dict[pi] == pr:
        print "pi", pi
        break

######## calculate index of machines  ######## 

m = int(input("number of machines:"))

if (m >= 400) and (m <2000):
    mr = np.round(m/50)*50
else:
    print "error, out of scope"
    sys.exit(1) 

m_dict = np.linspace(400,2000,33)

for mi in range(len(m_dict)):
    if m_dict[mi] == mr:
        print "mi", mi
        break

######## lookup production cost ######## 

i = pi*10 + mi

#######  50     60     70     80     90     100    120    140    160    180    200   #######
ca   = [47.78, 48.61, 49.32, 49.94, 50.49, 51.01, 51.88, 52.64, 53.31, 53.89, 54.44, #     400 
        45.89, 46.69, 47.37, 47.97, 48.51, 48.99, 49.83, 50.56, 51.21, 51.77, 52.28, #     450 
        44.27, 45.03, 45.69, 46.27, 46.78, 47.25, 48.07, 48.77, 49.38, 49.93, 50.43, #     500 
        42.85, 43.59, 44.22, 44.78, 45.28, 45.73, 46.52, 47.21, 47.79, 48.33, 48.81, #     550 
        41.59, 42.31, 42.92, 43.47, 43.95, 44.39, 45.16, 45.82, 46.39, 46.91, 47.38, #     600 
        40.46, 41.16, 41.76, 42.29, 42.76, 43.19, 43.94, 44.58, 45.14, 45.64, 46.11, #     650 
        39.45, 40.13, 40.72, 41.23, 41.69, 42.11, 42.83, 43.46, 44.01, 44.50, 44.94, #     700 
        38.53, 39.19, 39.77, 40.27, 40.72, 41.12, 41.83, 42.44, 42.98, 43.46, 43.89, #     750 
        37.69, 38.34, 38.89, 39.39, 39.83, 40.22, 40.92, 41.52, 42.04, 42.51, 42.93, #     800 
        36.91, 37.55, 38.09, 38.58, 39.01, 39.40, 40.08, 40.66, 41.18, 41.64, 42.05, #     850 
        36.21, 36.82, 37.36, 37.83, 38.25, 38.63, 39.31, 39.88, 40.38, 40.83, 41.24, #     900 
        35.53, 36.15, 36.67, 37.14, 37.55, 37.92, 38.58, 39.14, 39.64, 40.08, 40.48, #     950 
        34.91, 35.52, 36.04, 36.49, 36.89, 37.26, 37.91, 38.46, 38.95, 39.38, 39.77, #    1000 
        34.33, 34.93, 35.44, 35.89, 36.29, 36.65, 37.28, 37.82, 38.29, 38.73, 39.11, #    1050 
        33.79, 34.38, 34.88, 35.32, 35.71, 36.07, 36.69, 37.23, 37.69, 38.12, 38.51, #    1100 
        33.28, 33.86, 34.35, 34.79, 35.17, 35.52, 36.14, 36.66, 37.13, 37.54, 37.91, #    1150 
        32.79, 33.37, 33.85, 34.28, 34.66, 35.01, 35.61, 36.13, 36.59, 37.01, 37.37, #    1200 
        32.34, 32.89, 33.38, 33.81, 34.18, 34.52, 35.12, 35.63, 36.08, 36.48, 36.85, #    1250 
        31.91, 32.46, 32.94, 33.35, 33.73, 34.06, 34.65, 35.16, 35.61, 36.01, 36.36, #    1300 
        31.49, 32.05, 32.52, 32.93, 33.29, 33.62, 34.21, 34.71, 35.14, 35.54, 35.89, #    1350 
        31.11, 31.65, 32.11, 32.52, 32.88, 33.21, 33.78, 34.28, 34.71, 35.11, 35.44, #    1400 
        30.74, 31.27, 31.73, 32.13, 32.49, 32.81, 33.38, 33.87, 34.29, 34.68, 35.02, #    1450 
        30.39, 30.91, 31.36, 31.76, 32.11, 32.43, 32.99, 33.48, 33.89, 34.28, 34.62, #    1500 
        30.05, 30.57, 31.01, 31.39, 31.75, 32.07, 32.63, 33.09, 33.52, 33.89, 34.23, #    1550 
        29.72, 30.24, 30.68, 31.07, 31.41, 31.72, 32.27, 32.74, 33.16, 33.53, 33.86, #    1600 
        29.41, 29.92, 30.36, 30.74, 31.08, 31.39, 31.93, 32.40, 32.81, 33.17, 33.51, #    1650 
        29.11, 29.61, 30.05, 30.43, 30.77, 31.07, 31.61, 32.07, 32.48, 32.84, 33.16, #    1700 
        28.82, 29.32, 29.75, 30.13, 30.46, 30.76, 31.31, 31.75, 32.15, 32.51, 32.84, #    1750 
        28.55, 29.04, 29.46, 29.84, 30.17, 30.47, 31.01, 31.45, 31.85, 32.19, 32.52, #    1800 
        28.28, 28.77, 29.19, 29.56, 29.89, 30.18, 30.71, 31.16, 31.55, 31.89, 32.22, #    1850 
        28.02, 28.51, 28.92, 29.29, 29.62, 29.91, 30.43, 30.87, 31.26, 31.61, 31.92, #    1900 
        27.77, 28.26, 28.67, 29.03, 29.35, 29.65, 30.16, 30.60, 30.99, 31.33, 31.64, #    1950 
        27.54, 28.01, 28.42, 28.78, 29.09, 29.39, 29.89, 30.33, 30.72, 31.06, 31.37] #    2000 

cost = ca[i]

print "cost = ", cost

