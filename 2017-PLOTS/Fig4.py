import os
import sys
sys.path.append("/usr/bin") # necessary for the tex fonts
sys.path.append("../Python modules/") # necessary for the tex fonts
import scipy as sp
import scipy.misc
import matplotlib
import matplotlib.pyplot as plt
import h5py
import numpy as np
#from BackgroundCorrection import *
#from TConversionThermocoupler import *
import matplotlib.cm as cm
import scipy.ndimage as ndimage
#from matplotlib_scalebar.scalebar import ScaleBar #### Has issue with plotting using latex font. only import when needed, then unimport
#from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.backends.backend_pdf import PdfPages
from MakePdf import *
from matplotlib.pyplot import cm #to plot following colors of rainbow
from matplotlib import rc
#from CreateDatasets import *
import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)
warnings.simplefilter(action = "ignore", category = DeprecationWarning)
warnings.simplefilter(action = "ignore", category = FutureWarning)
warnings.simplefilter(action = "ignore", category = PendingDeprecationWarning)
from Registration import * 
from tifffile import *
from sklearn.mixture import GMM 
import matplotlib.cm as cm
#from FluoDecay import *
#from PlottingFcts import *
from mpl_toolkits.axes_grid1 import make_axes_locatable
import scipy.misc
import matplotlib.animation as animation
import gc
import tempfile
from tempfile import TemporaryFile

import skimage
from skimage import exposure
from my_fits import *

import pickle
import my_fits
from uncertainties import unumpy
from numpy import genfromtxt

### settings
fsizepl = 24
fsizenb = 20
mkstry = ['8','11','5'] #marker size for different dsets Med Zoom/Large Zoom/Small Zoom
dpi_no=80
sizex = 8
sizey =6
###
sizex = 8
sizey=3

fig1= plt.figure(figsize=(sizex, sizey), dpi=dpi_no)
fig1.set_size_inches(1200./fig1.dpi,900./fig1.dpi)
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', serif='Palatino')    

noplots = 2
nolines = 2

ax3 = plt.subplot2grid((nolines,noplots), (0,0), colspan=1, rowspan=1)
ax3.text(-0.1, 1.0, 'a', transform=ax3.transAxes,fontsize=fsizepl, fontweight='bold', va='top', ha='right', 
         bbox={'facecolor':'None', 'pad':5})

sys.path.append("../2017-01-19_Combining_data_Andrea/") # necessary 
from Combining_data_with_prefix_onlyIntensVisibRatio import do_pic
do_pic(ax3,fig1)

from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
ax4 = host_subplot(222, axes_class=AA.Axes)
ax4.text(+1.1, 1.0, 'c', transform=ax4.transAxes,fontsize=fsizepl, fontweight='bold', va='top', ha='right', bbox={'facecolor':'None', 'pad':5})

#ax4 = plt.subplot2grid((nolines,noplots), (0,1), colspan=1, rowspan=1)
sys.path.append("../2017-01-19_Combining_data_Andrea/") # necessary 
from Combining_data_with_prefix_onlyIntensVisibRatio import do_visib_other_qttties
do_visib_other_qttties(ax4)
ax4.axis["top"].set_visible(False)
ax4.axis["left"].set_visible(False)

ax30 = plt.subplot2grid((nolines,noplots), (1,0), colspan=1, rowspan=1)
ax30.text(-0.1, 1.0, 'b', transform=ax30.transAxes,fontsize=fsizepl, fontweight='bold', va='top', ha='right', 
         bbox={'facecolor':'None', 'pad':5})

#Fitted C = 17.23
#Fitted DE = 0.425065
def deriv(DE, k, T, C):
    
    return DE/(k * (T+273.15)**2)/(1 + np.cosh(DE/(k * (T+273.15)) - C))
    
T = np.linspace(30,60,50)
T2 = np.linspace(25,65,50)
ax30.plot(T,100.0*deriv(0.425065,8.617*1.0e-5,T,17.23),lw=2,color='k',ls='--')
ax30.spines['right'].set_visible(False)
ax30.spines['top'].set_visible(False)
ax30.xaxis.set_ticks_position('bottom')
ax30.yaxis.set_ticks_position('left')
ax30.set_ylabel(r'$\partial$(visibility)/$\partial$T ($\%$ $^{\circ}$C$^{-1}$)',fontsize=fsizepl)
ax30.set_xlabel('Temperature at heater ($^{\circ}$C)',fontsize=fsizepl)
ax30.tick_params(labelsize=fsizenb)
ax30.set_ylim([0.6,2.2])
ax30.set_xlim([25, 65])
ax30.set_xticks([30,40,50,60]) 
ax30.set_yticks([1,1.5,2.0])
ax30.fill_between(T2,0.5,1.5, color =[168/256,175/256,175/256],edgecolor='k',
                         facecolor=[168/256,175/256,175/256],
                         alpha=0.5,
                         linewidth=0.0)
ax30.text(37,1.0, 'previously reported \n (fluorescence ratio of intensity)', fontsize=fsizenb, va='center',ha='center')


plt.tight_layout()
   
multipage_longer_desired_aspect_ratio('Fig4.pdf',1600,1200,dpi=80,)


