# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 14:37:21 2016

@author: clarice
"""

import numpy as np
import matplotlib.pyplot as plt
#from sklearn.mixture import GMM 
import matplotlib.cm as cm
#from matplotlib_scalebar.scalebar import ScaleBar
import lmfit
from lmfit import minimize, Parameters, Parameter, report_fit

plt.close('all')

#x_array[:-6]*time_detail from other file
x0 = np.array([ 0.  ,  0.05,  0.1 ,  0.15,  0.2 ,  0.25,  0.3 ,  0.35,  0.4 ,
        0.45,  0.5 ,  0.55,  0.6 ,  0.65,  0.7 ,  0.75,  0.8 ,  0.85,
        0.9 ,  0.95,  1.  ,  1.05,  1.1 ,  1.15,  1.2 ,  1.25,  1.3 ,
        1.35,  1.4 ,  1.45,  1.5 ,  1.55,  1.6 ,  1.65,  1.7 ,  1.75,
        1.8 ,  1.85,  1.9 ,  1.95,  2.  ,  2.05,  2.1 ,  2.15,  2.2 ,
        2.25,  2.3 ,  2.35,  2.4 ,  2.45,  2.5 ,  2.55,  2.6 ,  2.65,
        2.7 ,  2.75,  2.8 ,  2.85,  2.9 ,  2.95,  3.  ,  3.05,  3.1 ,
        3.15,  3.2 ,  3.25,  3.3 ,  3.35,  3.4 ,  3.45,  3.5 ,  3.55,
        3.6 ,  3.65,  3.7 ,  3.75,  3.8 ,  3.85,  3.9 ,  3.95,  4.  ,
        4.05,  4.1 ,  4.15,  4.2 ,  4.25,  4.3 ,  4.35,  4.4 ,  4.45,
        4.5 ,  4.55,  4.6 ,  4.65,  4.7 ,  4.75,  4.8 ,  4.85,  4.9 ,
        4.95,  5.  ,  5.05,  5.1 ,  5.15,  5.2 ,  5.25,  5.3 ,  5.35,
        5.4 ,  5.45,  5.5 ,  5.55,  5.6 ,  5.65,  5.7 ,  5.75,  5.8 ,
        5.85,  5.9 ,  5.95,  6.  ,  6.05,  6.1 ,  6.15,  6.2 ,  6.25,
        6.3 ,  6.35,  6.4 ,  6.45,  6.5 ,  6.55,  6.6 ,  6.65,  6.7 ,
        6.75,  6.8 ,  6.85,  6.9 ,  6.95,  7.  ,  7.05,  7.1 ,  7.15,
        7.2 ,  7.25,  7.3 ,  7.35,  7.4 ,  7.45,  7.5 ,  7.55,  7.6 ,
        7.65,  7.7 ,  7.75,  7.8 ,  7.85,  7.9 ,  7.95,  8.  ,  8.05,
        8.1 ,  8.15,  8.2 ,  8.25,  8.3 ,  8.35,  8.4 ,  8.45,  8.5 ,
        8.55,  8.6 ,  8.65,  8.7 ,  8.75,  8.8 ,  8.85,  8.9 ,  8.95,
        9.  ,  9.05,  9.1 ,  9.15,  9.2 ,  9.25,  9.3 ,  9.35,  9.4 ,
        9.45,  9.5 ,  9.55,  9.6 ,  9.65])

#sum_grana_blue[6:]/1000.0/No_specimen
y0 = np.array([ 193.17333333,  191.14666667,  173.54666667,  165.33333333,
        147.52      ,  136.74666667,  128.42666667,  126.72      ,
        124.58666667,  105.81333333,  109.44      ,  104.74666667,
        100.8       ,   93.76      ,   91.09333333,   83.94666667,
         83.2       ,   82.24      ,   78.08      ,   74.98666667,
         73.38666667,   69.01333333,   73.17333333,   69.01333333,
         62.82666667,   60.48      ,   61.33333333,   59.2       ,
         59.84      ,   54.50666667,   58.02666667,   56.32      ,
         53.12      ,   49.06666667,   45.01333333,   49.06666667,
         44.8       ,   45.65333333,   45.33333333,   38.29333333,
         42.98666667,   41.92      ,   35.84      ,   41.81333333,
         40.74666667,   37.01333333,   35.62666667,   38.18666667,
         37.76      ,   39.25333333,   35.52      ,   34.66666667,
         32.85333333,   35.62666667,   29.12      ,   29.54666667,
         27.94666667,   34.24      ,   30.93333333,   32.42666667,
         32.32      ,   28.37333333,   29.12      ,   28.58666667,
         29.54666667,   25.92      ,   24.42666667,   25.70666667,
         26.34666667,   25.70666667,   26.56      ,   28.26666667,
         24.53333333,   26.88      ,   23.36      ,   22.93333333,
         24.42666667,   22.61333333,   22.18666667,   21.22666667,
         25.38666667,   21.65333333,   22.4       ,   21.97333333,
         23.46666667,   21.01333333,   21.54666667,   24.10666667,
         18.98666667,   19.30666667,   19.84      ,   18.88      ,
         18.02666667,   17.38666667,   19.73333333,   18.02666667,
         16.85333333,   20.37333333,   19.09333333,   16.53333333,
         19.2       ,   17.70666667,   19.62666667,   18.77333333,
         17.38666667,   15.57333333,   16.74666667,   16.85333333,
         17.28      ,   15.46666667,   17.49333333,   16.        ,
         15.89333333,   16.        ,   18.88      ,   18.13333333,
         17.49333333,   16.10666667,   14.50666667,   16.42666667,
         15.57333333,   15.68      ,   16.74666667,   14.82666667,
         14.50666667,   13.97333333,   15.89333333,   14.4       ,
         17.28      ,   14.18666667,   16.74666667,   13.44      ,
         11.62666667,   12.90666667,   13.44      ,   14.4       ,
         12.69333333,   15.14666667,   15.78666667,   13.01333333,
         16.        ,   13.22666667,   13.44      ,   13.54666667,
         11.2       ,   13.86666667,   12.48      ,   14.72      ,
         14.82666667,   13.22666667,   13.01333333,   14.50666667,
         11.30666667,   13.65333333,   12.8       ,   12.8       ,
         13.22666667,   11.94666667,   13.76      ,   13.44      ,
         11.2       ,   14.18666667,   11.73333333,   13.22666667,
         10.88      ,   11.52      ,   13.97333333,   10.56      ,
         12.26666667,   14.50666667,   15.14666667,   13.54666667,
         15.14666667,   11.2       ,   12.26666667,   10.13333333,
         13.22666667,   10.88      ,   11.94666667,   12.37333333,
         10.88      ,   13.12      ,   13.12      ,   12.37333333,
         10.13333333,   10.98666667,   11.41333333,    9.92      ,
         11.41333333,   11.62666667,   10.88      ,   12.16      ,
         10.24      ,   13.76      ])




def fcn2min(params, x, data, return_plot = False, no_of_x_pts = 100, single = False):

    a = params['a'].value
    b = params['b'].value
    c = params['c'].value
    
    if single == False:
        d = params['d'].value
        e = params['e'].value

    if return_plot == True:
        # changing x to give more values
        x = np.linspace(np.min(x), np.max(x), no_of_x_pts)
        
    model = a*np.exp(-x/b) + c + d*np.exp(-x/e)  
     
    if return_plot == False:
        return model - data
    else:
        return (x, model)
        
        




cutl = 15

cutr = 25



x = x0[0:cutl]
y = y0[0:cutl]


plt.close('all')


plt.plot(x0, y0, 'ko')


# create a set of Parameters
params = Parameters()
params.add('a', value= 112.0, min=0.0,max=200.0)
params.add('b', value= 2.0, min=0.0,max=400.0)
params.add('c', value= 12.0, min=0.0,max=60.0, vary=False)

params.add('d', value= 0.0, min=0.0,max=50.0, vary=False)
params.add('e', value= 150.0, min=0.0,max=200.0, vary=False)
    
result = minimize(fcn2min, params, args=(x, y))
(x_fit, y_fit) = fcn2min(result.params, x,y, return_plot = True)

report_fit(result.params)
plt.plot(x, y, 'ro')
#plt.plot(x0, y0, 'ko')
plt.plot(x_fit, y_fit, 'b')




x = x0[cutr:]
y = y0[cutr:]


#plt.close('all')


# create a set of Parameters
params = Parameters()
params.add('a', value= 20.0, min=0.0,max=150.0)
params.add('b', value= 321.0, min=0.0,max=400.0)
params.add('c', value= 1.0, min=0.0,max=60.0, vary=True)

params.add('d', value= 0.0, min=0.0,max=50.0, vary=False)
params.add('e', value= 150.0, min=0.0,max=200.0, vary=False)
    
result = minimize(fcn2min, params, args=(x, y))
(x_fit, y_fit2) = fcn2min(result.params, np.append(0, x), np.append(0, y), return_plot = True)

report_fit(result.params)
plt.plot(x, y, 'ro')
plt.plot(x_fit, y_fit2, 'b')


plt.plot(x_fit, y_fit + y_fit2 - result.params['c'].value, 'g')

plt.show()



