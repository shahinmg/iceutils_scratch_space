#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 11:47:56 2022

@author: laserglaciers
"""

import iceutils as ice
import rasterio
import os
import rioxarray
import rasterio
import numpy as np

vel_path = '../velocity/'
ice_thickness_path = '../bed_machine_products/ice_thickness_clip_s2_its_live_same_extent_clip.tif'
bed_path = '../bed_machine_products/bed_clip_s2_its_live_same_extent_clip.tif'

bed_src = rasterio.open(bed_path) 
bed = bed_src.read(1)

ice_H_src = rasterio.open(ice_thickness_path) 
ice_thickness = ice_H_src.read(1)

vel_list = [vel for vel in os.listdir(vel_path) if vel.endswith('nc')]

op = '/media/laserglaciers/konoha/its_live/helheim_its_live_s2_stress/'

os.chdir(vel_path)
vx_r = rasterio.open(f'{vel_path}S2A_24WWU_20190807_0_L1C_X_S2A_24WWU_20190817_0_L1C_G0120V02_P082_vx_fill_clip.tif')
vy_r = rasterio.open(f'{vel_path}S2A_24WWU_20190807_0_L1C_X_S2A_24WWU_20190817_0_L1C_G0120V02_P082_vy_fill_clip.tif')

vx = vx_r.read(1)
vy = vy_r.read(1)

strain_dict, stress_dict = ice.compute_stress_strain(vx, vy,rotate=True,h=ice_thickness,b=bed)

e_xx = strain_dict['e_xx']
e_yy = strain_dict['e_yy']
e_xy = strain_dict['e_xy'] #original shear_strain

# shear strain test
vx_gradient = np.gradient(vx)
vy_gradient = np.gradient(vy)

dx = vx_r.transform[0]
dy = vx_r.transform[4]

e_xy_v2 = (0.5*((vx_gradient[0]/dy) + (vy_gradient[0]/dx)))
theta = np.arctan2(vx,vy) 
e_xy_rot_v2 = (-e_xx*np.sin(theta)*np.cos(theta)) + (e_yy*np.sin(theta)*np.cos(theta))+(e_xy_v2*(2*(np.cos(theta)**2) - (1)))

dilatation = strain_dict['dilatation']
effective = strain_dict['effective']


eta = stress_dict['eta']
t_xx = stress_dict['t_xx']
t_xy = stress_dict['t_xy']
t_yy = stress_dict['t_yy']


tmxx = stress_dict['tmxx']
tmxy = stress_dict['tmxy'] 
tmyy = stress_dict['tmyy'] 
tmyx = stress_dict['tmyx']
tdx = stress_dict['tdx']
tdy = stress_dict['tdy']


band_description = ['eta', 't_xx','t_xy','t_yy', 'tmxx', 'tmxy', 'tmyy','tmyx','tdx', 'tdy']
bands = [eta, t_xx, t_xy, t_yy, tmxx, tmxy, tmyy, tmyx, tdx, tdy]

driving_stress_bands = [tdx,tdy]
driving_stress_bands_name = ['tdx', 'tdy']

meta = {'count':2,
        'crs':vx_r.crs,
        'driver': 'GTiff',
        'dtype': 'float32',
        'nodata':vx_r.nodata,
        'transform': vx_r.transform,
        'height':vx_r.height,
        'width':vx_r.width
    }

op = '../output/'
fn = 'S2A_24WWU_20190807_0_L1C_X_S2A_24WWU_20190817_0_L1C_G0120V02_P082_driving_stress.tif'
with rasterio.open(f'{op}{fn}',mode='w',**meta) as dst:
    for band_num, band in enumerate(driving_stress_bands, start=1):
        dst.write(band,band_num)
        dst.set_band_description(band_num, driving_stress_bands_name[band_num-1])


strain_rate_bands = [e_xx,e_yy, e_xy_rot_v2, e_xy]
strain_rate_bandsname = ['e_xx', 'e_yy', 'e_xy_rot_v2', 'e_xy']
meta_strain_rate = {'count':4,
        'crs':vx_r.crs,
        'driver': 'GTiff',
        'dtype': 'float32',
        'nodata':vx_r.nodata,
        'transform': vx_r.transform,
        'height':vx_r.height,
        'width':vx_r.width
    }



fn = 'S2A_24WWU_20190807_0_L1C_X_S2A_24WWU_20190817_0_L1C_G0120V02_P082_strain_rate_test.tif'
with rasterio.open(f'{op}{fn}',mode='w',**meta_strain_rate) as dst:
    for band_num, band in enumerate(strain_rate_bands, start=1):
        dst.write(band,band_num)
        dst.set_band_description(band_num, strain_rate_bandsname[band_num-1])


bed_src.close()
vx_r.close()
vy_r.close()