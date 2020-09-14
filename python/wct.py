#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from sklearn.cluster import MiniBatchKMeans
import rasterio as rio
import numpy as np
from skimage.filters import threshold_otsu
from python.misc import compute_index
from rasterio.plot import reshape_as_image

def compute_cluster(img,k=3,random_seed=42):

    """
	Computes cluster based on input image (stack).
    """

    img_float = img.astype(np.float32)/10000
    samples = reshape_as_image(img_float).reshape(-1,img_float.shape[0])
    kmeans_pred = MiniBatchKMeans(n_clusters=k+1, 
                                  random_state=random_seed,
                                  max_iter=10,
                                  batch_size=10000,
                                  reassignment_ratio=0).fit(samples)
    
    return kmeans_pred.labels_.reshape(img.shape[1], img.shape[2]).astype(rio.uint16)

def compute_rws(mndwi_img,mgrn_img,thr=0.3):

	"""
	Computes Reliable Water Sample (RWS) region after (Chen et al.,2020).
	Requires MNDWI and MGRN images. 
    """

	
    if thr == 'otsu':
        thr = threshold_otsu(mndwi_img[mndwi_img>=0])
    
    return np.where( (mndwi_img>=thr) &((mgrn_img>0) & (mgrn_img<0.15)),1,0)

def compute_mnws(img,cluster_img):

	"""
	Computes Minimum Normalized Water Score (MNWS) image after (Chen et al.,2020).
	Requires input band image (stack) and clustered image.
    """

    if len(img.shape) > 2 and img.shape[0] > 2:
        np.seterr(divide='ignore', invalid='ignore')

        mnws = []

        max_i = np.argmax(np.unique(cluster_img,return_counts=True)[1])
        all_labels = list(range(0,cluster_img.max()+1))
        labels = list(set(all_labels)-set([all_labels[max_i]]))

        for label in labels:

            #calculate band stats
            region_img = np.where(cluster_img==label,img,0)
            band_means = np.array(list(map(lambda x:np.mean(region_img[x][region_img[x]!=0],dtype=np.float32),
                                           range(img.shape[0])))).reshape(img.shape[0],-1)
            band_std = np.array(list(map(lambda x:np.std(region_img[x][region_img[x]!=0],dtype=np.float32),
                                         range(img.shape[0])))).reshape(img.shape[0],-1)

            #calculate nws 
            reshaped_img = img.reshape(img.shape[0],-1)
            nws = (((( abs(reshaped_img-band_means) /band_std)**2).sum(0)/img.shape[0])**0.5).reshape(img.shape[1],img.shape[2])
            mnws.append(nws)

        mnws_img = np.array(mnws).min(0)

        return mnws_img
    
def render_wcf(mnws_files,invalid_files,upland_file,thr=3,dec=2):

	"""
	Computes Water Coverage Frequency (WCF) image after (Chen et al.,2020).
	Requires path of MNWS image files, invalid pixel mask files and terrain (upland) mask file. 
    """
    
    with rio.open(upland_file) as src_upland:
        upland_mask = src_upland.read(1)
    
        water_rws_detected = []
        invalid_pixels = []    

        for i in tqdm(range(len(mnws_files)),position=0, leave=True):
            mnws_file = mnws_files[i]
            cl_mask_file = invalid_files[i]

            with rio.open(mnws_file) as src_mnws,rio.open(cl_mask_file ) as src_mask:
                profile = src_mnws.profile.copy()
                mnws_img = src_mnws.read(1)
                mnws_img[np.isnan(mnws_img)]=9999

                cl_mask = src_mask.read(1)

                invalid = np.where(cl_mask==2,1,0)
                invalid_pixels.append(invalid)

                water_rws = np.where(mnws_img<=thr,1,0)

                water_rws = np.where( cl_mask>0,0,water_rws)
                water_rws_detected.append(water_rws)

        water_rws_detected_sum = np.where(upland_mask==1,0,np.array(water_rws_detected).sum(0))
        invalid_pixels_sum = np.array(invalid_pixels).sum(0)
        diff_invalid = len(mnws_files)-invalid_pixels_sum

        water_freq_img = np.true_divide(water_rws_detected_sum , diff_invalid, where=(diff_invalid!=0),dtype=np.float32)*12
        water_freq_img_r = np.round(water_freq_img,dec)

        return water_freq_img_r,water_rws_detected_sum,profile

