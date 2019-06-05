 #!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 20:08:43 2019

@author: corey.austin
"""
#%%
import numpy as np
from matplotlib import pyplot as plt
from gwpy.timeseries import TimeSeries
import seaborn as sns

#%%
#suspoint = TimeSeries.fetch('L1:OAF-SUSPOINT_INF_ITMX_L_OUTPUT',
#                            'May 31 2019 00:00:00 UTC','May 31 2019 00:17:00 UTC')
#suspoint.write('suspoint.hdf5',overwrite=True)

#ground = TimeSeries.fetch('L1:ISI-GND_STS_ITMX_X_DQ',
#                            'May 31 2019 00:00:00 UTC','May 31 2019 00:17:00 UTC')
#ground.write('suspoint.hdf5',overwrite=True)
        
suspoint = TimeSeries.read('suspoint.hdf5')
suspoint_asd = suspoint.asd(100,50)
suspoint_asd *= 1e-9


ground = TimeSeries.read('ground.hdf5') 
ground_asd = ground.asd(100,50)
ground_asd *= 1e-9/(2*np.pi*ground_asd.frequencies)

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
