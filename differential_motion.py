 #!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 20:08:43 2019

@author: corey.austin
"""
#%%
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
import cmath
from gwpy.timeseries import TimeSeries
import seaborn as sns

class transferFunction:
    
    def magPhase(self):
        self.magdb = 20*np.log10(abs(self.cplx))
        self.phase = np.zeros(len(self.cplx))
        for i in xrange(len(self.cplx)):
            self.phase[i] = cmath.phase(self.cplx[i])*180/np.pi  
    
    def loadFile(self,file,fnew):
        data = np.loadtxt(file)
        self.freq = fnew
        freq = data[:,0]
        real = data[:,1]
        imag = data[:,2]*1j
        f1 = interp1d(freq,real,fill_value='extrapolate')
        self.real = f1(fnew)
        f2 = interp1d(freq,imag,fill_value='extrapolate')
        self.imag = f2(fnew)
        self.cplx = self.real + self.imag
        self.magPhase()
        
    def bodePlot(self,title='Transfer Function'):
        plt.style.use('default')

        f1, (ax1,ax2) = plt.subplots(2,figsize=[16,9])  
        
        ax1.plot(self.freq,self.magdb)
        ax1.set_xlabel('Frequency (Hz)',fontsize=14,color='dimgrey')
        ax1.set_ylabel('Magnitude (dB)',fontsize=14,color='dimgrey')
        ax1.grid(which='both',axis='both',color='darkgrey',linestyle='dotted')
        ax1.set_xscale('log')
        
        ax2.plot(self.freq,self.phase)
        ax2.set_xlabel('Frequency (Hz)',fontsize=14,color='dimgrey')
        ax2.set_ylabel('Phase (Deg)',fontsize=14,color='dimgrey')
        ax2.grid(which='both',axis='both',color='darkgrey',linestyle='dotted')
        ax2.set_xscale('log')
        f1.suptitle(title,fontsize=18,color='dimgrey')
        
        plt.tight_layout(rect=[0,0,1,0.95])

#%%
#stage2 = TimeSeries.fetch('L1:ISI-ITMX_ST2_BLND_X_GS13_CUR_IN1_DQ',
#                          'May 31 2019 00:00:00 UTC','May 31 2019 00:17:00 UTC')
#suspoint = TimeSeries.fetch('L1:OAF-SUSPOINT_INF_ITMX_L_OUTPUT',
#                            'May 31 2019 00:00:00 UTC','May 31 2019 00:17:00 UTC')
#stage2.write('stage2.hdf5',overwrite=True)
#suspoint.write('suspoint.hdf5',overwrite=True)
        
stage2 = TimeSeries.read('stage2.hdf5')
suspoint = TimeSeries.read('suspoint.hdf5')

stage2_asd = stage2.asd(100,50)
stage2_asd *= 1e-9/(2*np.pi*stage2_asd.frequencies)
suspoint_asd = suspoint.asd(100,50)
suspoint_asd *= 1e-9


ground = TimeSeries.read('ground.hdf5') 
ground_asd = ground.asd(100,50)
ground_asd *= 1e-9/(2*np.pi*ground_asd.frequencies)
#fnew = ground_asd.frequencies.value
#
#isi_st1 = transferFunction()
#isi_st2 = transferFunction()
#total   = transferFunction()
#
#isi_st1.loadFile('isi_st1_tf.txt',fnew)
#isi_st2.loadFile('isi_st2_tf.txt',fnew)
#
#total.cplx = isi_st1.cplx * isi_st2.cplx
#total.freq = fnew
#total.magPhase()
#
##isi_st1.bodePlot(title='Stage 1 Filter')
##isi_st2.bodePlot(title='Stage 2 Filter')
#total.bodePlot(title='Stage 1 + Stage 2 Filters')

#itm_asd = abs(ground_asd * total.cplx)
diff = np.sqrt((suspoint_asd.value - ground_asd.value[0:801])**2)




#%%
plt.style.use('seaborn-whitegrid')

f1,ax1 = plt.subplots(1,figsize=[16,9])  

ax1.set_prop_cycle('color',sns.color_palette('bright'))
ax1.grid(which='both',axis='both',color='darkgrey',linestyle='dotted')

ax1.plot(ground_asd,label='Ground (STS)')
ax1.plot(suspoint_asd,label='Suspoint')
ax1.plot(suspoint_asd.frequencies,diff,':',label='Differential')
ax1.set_xlabel('Frequency (Hz)',fontsize=14,color='dimgrey')
ax1.set_ylabel(r'$\rm{m}/\sqrt{\rm {Hz}}$',fontsize=14,color='dimgrey')
ax1.set_xlim([0.01,2])
ax1.set_ylim([5e-13,3e-5])
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_title('Differential Motion Between Ground and ITMX Suspoint')

ax1.legend(framealpha=0.1,frameon=True)
