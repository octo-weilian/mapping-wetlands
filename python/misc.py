#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import rasterio as rio
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from affine import Affine
import geopandas as gpd
import pandas as pd

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
    """
    Compute invalid pixel mask (cloud, cloud shadow  and land vegetation)
    Input image should be stacked in the following order ['B2','B3','B4','B8A','B11']
    """
    
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
    

def strat_rand_sampling(file,size,vstride_nr,nodat=0,seed=None):
    #set seed for numpy random 
    np.random.seed(seed)
    
    data = []
    with rio.open(file) as src:
        
        #translate rows, cols to xy coordinates
        T0 = src.transform
        T1 = T0 * Affine.translation(0.5, 0.5)
        rc2xy = lambda r, c: T1 * (c, r) 

        img = src.read(1)
        profile = src.profile.copy()
        block_img = img.copy()
        
        vstride = int(block_img.shape[0]/vstride_nr)
        
        for i in range(0,block_img.shape[0],vstride):
            random_label = int((i+vstride)/100)
            if i+vstride<block_img.shape[0]:
                block_img[i:i+vstride,:][block_img[i:i+vstride,:]>=0] = random_label
            else:
                block_img[i:,:][block_img[i:,:]>=0] = random_label
            
        stack_img = np.where(img>0,block_img,nodat).astype(rio.uint8)
        
        strata = np.unique(stack_img)[np.unique(stack_img)!=nodat]
        classes = np.unique(img)[np.unique(img)!=nodat]
        
        for grid in strata: 
            for c in classes:
                rows,cols = np.where((img==c)&(stack_img==grid))
        
                if len(rows)!=0:
                    idx = np.random.choice(range(len(cols)), size, replace=False)
                    stratified_samples = np.array([rc2xy(x, y) for x,y in zip(rows[idx],cols[idx]) ])
                    x,y = stratified_samples[:,0],stratified_samples[:,1]
                    gdf = gpd.GeoDataFrame(crs=str(src.crs), geometry=gpd.points_from_xy(x,y))
                    gdf['class'] = c
                    data.append(gdf)
        
        profile.update(nodata=0,dtype=rio.uint8)
        data_cat = pd.concat(data,ignore_index=True)
        return data_cat,stack_img,profile

def calc_acc(y_true,y_pred):
    
    observed = y_true.rename('Observed')
    classified = y_pred.rename('Classified')
    con_mat = pd.crosstab(classified,observed)
    
    row_sum = con_mat.sum(axis=1)
    col_sum = con_mat.sum(axis=0)
    omitted = np.setdiff1d(col_sum.index,row_sum.index)
    col_sum = col_sum.drop(omitted)
    
    ua = np.diag(con_mat)/row_sum
    pa = np.diag(con_mat)/col_sum
    f1 = (2 * pa*ua) /(pa+ua)
    
    acc_df = round(pd.DataFrame({'Label':col_sum.index,'PA':pa.values,'UA':ua.values,'F1-score':f1.values}),2).fillna(0)
    acc_df.set_index('Label',inplace=True)
    
    
    return acc_df,con_mat


def plot_acc(acc_df,con_mat,labels,oa_alt=None,fig_text=None):
    
    acc_df = acc_df.copy()
    con_mat = con_mat.copy()
    
    oa =np.diag(con_mat).sum()/con_mat.sum().sum()  

    sns.set(font_scale=1.5)
    sns.set_style('darkgrid',rc={"xtick.bottom" : True, "ytick.left" : True,'axes.edgecolor': '0'})

    fig, axs = plt.subplots(1,2,figsize=(12,5))

    con_mat.columns = [f'{b}\n{a}' for a,b in zip(labels,con_mat.sum(0))]
    con_mat.index = [f'{a}\n{b}' for a,b in zip(labels,con_mat.sum(1))]
    
    con_mat_plot = sns.heatmap(con_mat,annot=True,cbar=False,ax=axs[0],cmap='Blues')
    axs[0].set_xlabel('Observed')
    axs[0].set_ylabel('Classified')
    for _, spine in con_mat_plot.spines.items(): 
        spine.set_visible(True)
    
    acc_df.index = labels
    sns.lineplot(data=acc_df,ax=axs[1],dashes=False,sort=False)
    sns.scatterplot(data = acc_df,ax=axs[1])
    plt.ylim(0.35, 1)
    axs[1].set_ylabel('Accuracy')
    axs[1].set_xlabel('Label')
    
    leg = axs[1].legend(acc_df.columns.tolist()+[f'OA: { "%.2f" % oa} ({oa_alt}*)'],loc='best')
    leg.get_lines()[-1].set_visible(False)
    axs[0].text(-0.90,1.05,fig_text,horizontalalignment='center',verticalalignment='center',transform=axs[1].transAxes)
