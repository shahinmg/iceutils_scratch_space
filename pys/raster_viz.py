#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 10:47:52 2023

@author: laserglaciers
"""

import rasterio
import matplotlib.pyplot as plt
from rasterio.plot import show
from matplotlib import colors, cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

fig1, (ax1,ax2) = plt.subplots(1,2,figsize=(15,7),sharey=False)

td_r = rasterio.open('../output/S2A_24WWU_20190807_0_L1C_X_S2A_24WWU_20190817_0_L1C_G0120V02_P082_driving_stress.tif')
strain_r = rasterio.open('../output/S2A_24WWU_20190807_0_L1C_X_S2A_24WWU_20190817_0_L1C_G0120V02_P082_strain_rate_test.tif')

cmap = plt.get_cmap('seismic').copy()

e_xy_new = strain_r.read(3)
e_xy_original = strain_r.read(4)

# plot shear
vmin, vmax = -5,5
e_xy_new_img = show((strain_r,3),ax=ax1,cmap=cmap,vmin=vmin,vmax=vmax,title='edited')

e_xy_og_img = show((strain_r,4),ax=ax2,cmap=cmap, vmin=vmin, vmax=vmax, title='original e_xy')

divider = make_axes_locatable(ax2)
cax = divider.append_axes("right", size="5%", pad=0.1)
fig1.colorbar(cm.ScalarMappable(norm=colors.Normalize(vmin = vmin,vmax = vmax), cmap=cmap),
              cax=cax,label='e_xy')


#plot driving stress
fig2, ax_td = plt.subplots()
driving_stress_plot = show((td_r,1),ax=ax_td,cmap='viridis',vmin=0,vmax=50000,title='t_dx')

divider2 = make_axes_locatable(ax_td)
cax2 = divider2.append_axes("right", size="5%", pad=0.1)
fig2.colorbar(cm.ScalarMappable(norm=colors.Normalize(vmin = 0,vmax = 50000), cmap='viridis'),
              cax=cax2,label='t_dx')

plt.tight_layout()
td_r.close()
strain_r.close()


# save figs
fig1.savefig('../output/shear_strain_comparison.png')
fig2.savefig('../output/driving_stress_fig.png')
