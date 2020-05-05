# Mapping wetlands in East Africa  - Master (minor) thesis

<p align="center">
  <a>Cover image here<a/>
</p>

## Abstract
Text

Research questions/ objectives:
1. Text 
2. Text
3. Text 

## Repository content

<b>Python</b>  
* Contains all Python scripts used in the Jupyter Notebooks
	
<b>data</b>  
*  Contains all data and models used for analyses in Jupyter Notebook

<b>[00_download_preprocess_sentinel2.ipynb](https://github.com/octo-willy/Sargassum-Sensing/blob/master/00_download_preprocess_sentinel2.ipynb "00_download_preprocess_sentinel2.ipynb")</b>  
*  Notebook for downloading and pre-processing Sentinel-2 images	

<b>[01_sargassum_detection_coast.ipynb](https://github.com/octo-willy/Sargassum-Sensing/blob/master/01_sargassum_detection_coast.ipynb "01_sargassum_detection_coast.ipynb")</b>  
*  Notebook pertains to RQ 1
	
<b>[02_sargassum_detection_sea.ipynb](https://github.com/octo-willy/Sargassum-Sensing/blob/master/02_sargassum_detection_sea.ipynb "02_sargassum_detection_sea.ipynb")</b>  
*  Notebook pertains to RQ 2

<b>[03_seagrass_distribution_lacbay.ipynb](https://github.com/octo-willy/Sargassum-Sensing/blob/master/03_seagrass_distribution_lacbay.ipynb "03_seagrass_distribution_lacbay.ipynb")</b>  
*  Notebook pertains to RQ 3

<b>[xx_sargassum_sensing_demo.ipynb](https://github.com/octo-willy/Sargassum-Sensing/blob/master/xx_sargassum_sensing_demo.ipynb "xx_sargassum_sensing_demo.ipynb")</b>  
*  Notebook demonstrating Sargassum detection and forecasting in open sea

## Instructions
    
1. Clone or download repository
```shell 
> git clone git@github.com:octo-willy/Sargassum-Sensing.git
```
2. Install environment
```shell 
> conda env create -f environment.yml
```
3. Activate environment
```shell 
> activate sargassum
```
4. CD to repository and run notebook</b>
```shell 
> cd path_cloned_repository && jupyter notebook
```