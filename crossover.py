#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:50:50 2019

@author: coreyaustin
"""

#%%
import numpy as np
from matplotlib import pyplot as plt
from gwpy.timeseries import TimeSeries
import seaborn as sns

#%%
#accel = TimeSeries.fetch('L1:PEM-CS_ACC_BEAMTUBE_150X_X_DQ',
#                            'May 31 2019 00:00:00 UTC','May 31 2019 00:17:00 UTC')
#accel.write('accel.hdf5',overwrite=True)

#ground = TimeSeries.fetch('L1:ISI-GND_STS_ITMX_X_DQ',
#                            'May 31 2019 00:00:00 UTC','May 31 2019 00:17:00 UTC')
#ground.write('accel.hdf5',overwrite=True)

fftl = 100
ovlp = fftl/2
        
accel = TimeSeries.read('accel.hdf5')
#accel_asd = accel.asd(100,50)
accel_asd = accel.spectrogram2(fftlength=fftl,overlap=ovlp).percentile(50)**(1/2.)
accel_asd *= 6.1e-6/(4*np.pi**2*accel_asd.frequencies**2)
accel_idx = np.where(accel_asd.frequencies.value==6)

ground = TimeSeries.read('ground.hdf5') 
#ground_asd = ground.asd(100,50)
ground_asd = ground.spectrogram2(fftlength=fftl,overlap=ovlp).percentile(50)**(1/2.)
ground_asd *= 1e-9/(2*np.pi*ground_asd.frequencies)
ground_idx = np.where(ground_asd.frequencies.value==6)

flow = 500
fhigh = 700

average = np.zeros(len(accel_asd[flow:fhigh]))
for i in xrange(flow,fhigh):
    g_multi = fhigh - i
    a_multi = i - flow - 1
    average[i-flow] = (g_multi * ground_asd[i].value + a_multi * accel_asd[i].value) / (len(average) + 1)

combined_asd = np.concatenate((ground_asd.value[0:flow],average[0:len(average)],accel_asd.value[fhigh:]))

#%%
plt.style.use('seaborn-whitegrid')

f1,ax1 = plt.subplots(1,figsize=[16,9])  

ax1.set_prop_cycle('color',sns.color_palette('bright'))
ax1.grid(which='both',axis='both',color='darkgrey',linestyle='dotted')

ax1.plot(ground_asd,label=ground.channel)
ax1.plot(accel_asd,label=accel.channel)
ax1.plot(accel_asd.frequencies.value,combined_asd,label='Composite')
ax1.set_xlabel('Frequency (Hz)',fontsize=14,color='dimgrey')
ax1.set_ylabel(r'$\rm{m}/\sqrt{\rm {Hz}}$',fontsize=14,color='dimgrey')
ax1.set_xlim([1,60])
ax1.set_ylim([3e-12,2e-7])
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_title('Crossover Between Accelerometer and Seismometer')

ax1.legend(framealpha=0.1,frameon=True)
f1.tight_layout(rect=[0,0,.99,1])










