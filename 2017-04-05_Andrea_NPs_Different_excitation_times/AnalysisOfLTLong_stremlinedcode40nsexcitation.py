
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
import matplotlib.cm as cm
import scipy.ndimage as ndimage
from matplotlib.backends.backend_pdf import PdfPages
from MakePdf import *
from matplotlib.pyplot import cm #to plot following colors of rainbow
from matplotlib import rc
import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)
warnings.simplefilter(action = "ignore", category = DeprecationWarning)
warnings.simplefilter(action = "ignore", category = FutureWarning)
warnings.simplefilter(action = "ignore", category = PendingDeprecationWarning)
import matplotlib.cm as cm
import scipy.misc
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
from CreateDatasets import *
#PARAMS THAT NEED TO BE CHANGED
###############################################################################
###############################################################################
###############################################################################
#######

Time_bin = 1000#in ns; 
nominal_time_on = 40.0 #time during which e-beam nominally on, in mus
totaltrpoints = 500 #total number of time-resolved points

description = ['Andrea small NaYF4:Er'] # (20kV, 30$\mu$m, ' + str(Ps[index]) + 'nm pixels, ' + str(No_experiments[index]) + 'expts., InLens registered)'] #, \n' #+ obs[index] ']    
                                
No_experiments = 1*np.ones([5]) #50 avgs
nametr = ['2017-04-05-0925_ImageSequence__150.000kX_10.000kV_30mu_4']
let = ['ns40'] #no of pixels
#taken in the order above

######################################## Plot with dose for different apertures
##files below exist 

blue_int_array = np.zeros(len(nametr))
red_int_array = np.zeros(len(nametr))

blue_std_array = np.zeros(len(nametr))
red_std_array = np.zeros(len(nametr))

red_decay_array = np.zeros([len(nametr),498])
blue_decay_array = np.zeros([len(nametr),498])

bgblue_int_array = np.zeros(len(nametr))
bgred_int_array = np.zeros(len(nametr))

bgblue_std_array = np.zeros(len(nametr))
bgred_std_array = np.zeros(len(nametr))

bgred_decay_array = np.zeros([len(nametr),498])
bgblue_decay_array = np.zeros([len(nametr),498])

#pisize =Pixel_size

listofindex =np.arange(0,len(nametr))

consider_whole_light = [] 

ax0 = plt.subplot2grid((2,4), (0,0), colspan=1, rowspan=1)
ax1 = plt.subplot2grid((2,4), (0,1), colspan=1, rowspan=1)
ax2 = plt.subplot2grid((2,4), (0,2), colspan=1, rowspan=1)
ax2b = plt.subplot2grid((2,4), (0,3), colspan=1, rowspan=1)
ax3= plt.subplot2grid((2,4), (1,0), colspan=1, rowspan=1)
ax4 = plt.subplot2grid((2,4), (1,1), colspan=1, rowspan=1)
ax5 = plt.subplot2grid((2,4), (1,2), colspan=1, rowspan=1)

axvec = [ax0, ax1,ax2,ax2b, ax3,ax4,ax5]

#those cuts are ok
#original was 100x100 pixels
#current size (50, 1600, 118, 119)
xinit = [10 ] 
xend =  [-10 ]
yinit = [6] 
yend =  [-6]

listofindex =np.arange(0,len(nametr))
for index in listofindex:
    
    print(index)
    
    print('before loading')
    
    red0 = np.load(str(let[index]) +'Redbright.npz',mmap_mode='r')  
    se = np.load(str(let[index]) +'SEchannel.npz',mmap_mode='r') 
    
#    print(se['data'].shape)
    
    red = red0['data']

    del red0
    gc.collect()
    
    segmm, means, covars, weights = gmmone_tr_in_masked_channel_modif_memory_issue(se['data'][xinit[index]:xend[index],yinit[index]:yend[index]])#, red[:,:,xinit[index]:xend[index],yinit[index]:yend[index]]) 
    #############################################################
    red = red[:,:,xinit[index]:xend[index],yinit[index]:yend[index]]
   
    del means, covars, weights
    gc.collect()
    
    backgdinit = 13
    initbin = 52 #52 if 10+40=50 #202 if 50+150=200

    print('after skimage')
    
    #################
    
    #to plot the pics, uncomment 5 next lines
#    if True:
#        axvec[index].imshow(se['data'][xinit[index]:xend[index],yinit[index]:yend[index]],cmap=cm.Greys) #or 'OrRd'
#        axvec[index].imshow(segmm,cmap=cm.Greys)
#        print('after imshow')   
# #       del segmm, red, blue,se
#  #      gc.collect()
#multipage_longer('Checkcuts40ns.pdf',dpi=80)
#multipage_longer('Checksegmm40ns.pdf',dpi=80)
#klklkk  
#if True:
     
     #INSIDE
    if index in consider_whole_light:
         hlp = 1.0 #outside, consider all light
    else:
         hlp = np.copy(segmm)
         hlp[~np.isnan(hlp)] = 1.0  #inside
         #outside continues nan
     
     # OUTSIDE
    if index in consider_whole_light:
         hlpd  = 0.0 #consider all light
    else:
         hlpd = np.copy(segmm)
         hlpd[~np.isnan(hlpd)] = -5000.0 
         hlpd[np.isnan(hlpd)] = 1.0
         #added line
         hlpd[(hlpd == -5000.0)] = np.nan 
         
    del segmm
    gc.collect()
    
    print('red')
    red_int_array[index] = np.nanmean(red[:,backgdinit:initbin,:,:]*hlp,axis=(0,1,2,3)) 
    gc.collect()
    red_decay_array[index,:] = np.nanmean(red[:,initbin:,:,:]*hlp,axis=(0,2,3))
    gc.collect()
    red_std_array[index] = np.nanstd(red[:,backgdinit:initbin,:,:]*hlp,axis=(0,1,2,3)) 
    gc.collect()
    bgred_int_array[index] = np.nanmean(red[:,backgdinit:initbin,:,:]*hlpd,axis=(0,1,2,3)) 
    gc.collect()
    bgred_decay_array[index,:] = np.nanmean(red[:,initbin:,:,:]*hlpd,axis=(0,2,3))
    gc.collect()
    bgred_std_array[index] = np.nanstd(red[:,backgdinit:initbin,:,:]*hlpd,axis=(0,1,2,3))
    gc.collect()
    
    del red
    gc.collect()
    
    blue0 = np.load(str(let[index]) +'Bluebright.npz',mmap_mode='r')  
    blue = blue0['data']
    del blue0
    gc.collect()
    
    blue = blue[:,:,xinit[index]:xend[index],yinit[index]:yend[index]]
    
    print('blue')
    blue_int_array[index] = np.nanmean(blue[:,backgdinit:initbin,:,:]*hlp,axis=(0,1,2,3)) 
    gc.collect()
    blue_decay_array[index,:] = np.nanmean(blue[:,initbin:,:,:]*hlp,axis=(0,2,3))
    gc.collect()
    blue_std_array[index] = np.nanstd(blue[:,backgdinit:initbin,:,:]*hlp,axis=(0,1,2,3)) 
    gc.collect()
    bgblue_int_array[index] = np.nanmean(blue[:,backgdinit:initbin,:,:]*hlpd,axis=(0,1,2,3)) 
    gc.collect()
    bgblue_decay_array[index,:] = np.nanmean(blue[:,initbin:,:,:]*hlpd,axis=(0,2,3))
    gc.collect()
    bgblue_std_array[index] = np.nanstd(blue[:,backgdinit:initbin,:,:]*hlpd,axis=(0,1,2,3)) 
    gc.collect()

    del blue
    gc.collect()
 
#foreground
  
mycode = 'Red_std_arrayPixel = tempfile.NamedTemporaryFile(delete=False)'
exec(mycode)
np.savez('Red_std_arrayPixel', data = red_std_array)
 
mycode = 'Blue_std_arrayPixel = tempfile.NamedTemporaryFile(delete=False)'
exec(mycode)
np.savez('Blue_std_arrayPixel', data = blue_std_array)
 
mycode = 'Red_int_arrayPixel = tempfile.NamedTemporaryFile(delete=False)'
exec(mycode)
np.savez('Red_int_arrayPixel', data = red_int_array)
 
mycode = 'Blue_int_arrayPixel = tempfile.NamedTemporaryFile(delete=False)'
exec(mycode)
np.savez('Blue_int_arrayPixel', data = blue_int_array)
 
mycode = 'Red_decay_arrayPixel = tempfile.NamedTemporaryFile(delete=False)'
exec(mycode)
np.savez('Red_decay_arrayPixel', data = red_decay_array)

mycode = 'Blue_decay_arrayPixel = tempfile.NamedTemporaryFile(delete=False)'
exec(mycode)
np.savez('Blue_decay_arrayPixel', data = blue_decay_array)

###background

mycode = 'bgRed_std_arrayPixel = tempfile.NamedTemporaryFile(delete=False)'
exec(mycode)
np.savez('bgRed_std_arrayPixel', data = bgred_std_array)
 
mycode = 'bgBlue_std_arrayPixel = tempfile.NamedTemporaryFile(delete=False)'
exec(mycode)
np.savez('bgBlue_std_arrayPixel', data = bgblue_std_array)
 
mycode = 'bgRed_int_arrayPixel = tempfile.NamedTemporaryFile(delete=False)'
exec(mycode)
np.savez('bgRed_int_arrayPixel', data = bgred_int_array)
 
mycode = 'bgBlue_int_arrayPixel = tempfile.NamedTemporaryFile(delete=False)'
exec(mycode)
np.savez('bgBlue_int_arrayPixel', data = bgblue_int_array)

mycode = 'bgRed_decay_arrayPixel = tempfile.NamedTemporaryFile(delete=False)'
exec(mycode)
np.savez('bgRed_decay_arrayPixel', data =bgred_decay_array)

mycode = 'bgBlue_decay_arrayPixel = tempfile.NamedTemporaryFile(delete=False)'
exec(mycode)
np.savez('bgBlue_decay_arrayPixel', data = bgblue_decay_array)
    
kjjhjh
