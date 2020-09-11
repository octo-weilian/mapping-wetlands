#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import rasterio as rio
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def compute_index(left_band,right_band,name):
    np.seterr(divide='ignore', invalid='ignore')
    
    if name == 'MNDWI':
        b3= left_band.astype(np.float32)
        b11 = right_band.astype(np.float32)
        index = (b3-b11)/(b3+b11)

    elif name =='NDVI':
        b8a= left_band.astype(np.float32)
        b4=right_band.astype(np.float32)
        index = (b8a-b4)/(b8a+b4)
    
    return index

def compute_ipm(target_img,reference_img):
    """"
    Compute invalid pixel mask (cloud, cloud shadow  and land vegetation)
    Input image should be stacked in the following order ['B2','B3','B4','B8A','B11']
    """"
    
    np.seterr(divide='ignore', invalid='ignore')
    
    #compute cloud masks after using multitemporal cloud masking (MCM) method (Candra et al., 2020)
    db11 = target_img[4]-reference_img[4]
    db8a = target_img[3]-reference_img[3]
    db2 = target_img[2]-reference_img[2]
    db3 = target_img[1]-reference_img[1]
    db4 = target_img[0]-reference_img[0]
    
    #additional mask for land vegetation 
    ndvi_img = compute_index(target_img[3],target_img[2],'NDVI')
    
    #render masks into a single unified mask
    #cloud shadow = 1, thick cloud = 2, land vegetation = 3
    cl_shadow = np.where( (db8a<-400) & ( db11<-400 ),1,0)
    cl_thick = np.where( ((db2 > 800) & (db3 >800) & (db4 >800)),2,0)
    land_veg = np.where(ndvi_img>0.5,3,0)
       
    return np.amax(np.array([cl_shadow,cl_thick,land_veg]),0)
    

