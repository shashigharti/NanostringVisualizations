from os import listdir,path

import numpy as np
import cv2
import rasterio
from rasterio.transform import Affine
from rasterio.crs import CRS

def read_file(filename):
    "filename:full path to image"
    scan = np.flip(cv2.imread(filename),axis=0)
    return scan

def write_tif(base_name,Z):
    """
    Write image as separate georeferenced
    tif bands.
    args:
        base_name: output filename related
        Z: numpy array of shape [H,W,3]
    """
    if Z.ndim!=3:
        raise Exception("Not supported")
    n_channels = Z.shape[2]
    if n_channels<3:
        raise Exception("Not supported")
          
    transform = Affine.translation(0,0)*Affine.scale(10,10)
    metadata ={"driver":'GTiff',
               "height":Z.shape[0],
               "width":Z.shape[1],
               "count":1,
               "dtype":Z.dtype,
               "crs":CRS.from_epsg(3857),
               "transform":transform}
    
    output_filenames = [f"{base_name}_band{i}.tif" for i in range(3)]
    for i,filename in enumerate(output_filenames): 
        #Write band
        with rasterio.open(filename,'w',**metadata) as dst:
            dst.write(Z[...,i], 1)


def process_folder(data_path,output_path):
    filenames = [path.join(data_path,f) for f in listdir(data_path)]
    filenames = [file for file in filenames if file.endswith("scan.png")]
    
    for filename in filenames:
        print(f"Attaching coordinates to {path.basename(filename)}")
        scan = read_file(filename)
        base_name = path.splitext(path.basename(filename))[0]
        base_name = path.join(output_path,base_name)
        write_tif(base_name,scan)
        

if __name__=="__main__":

    data_folder = "ROI reports"
    output_folder = "raw_tifs"
    process_folder(data_folder,output_folder)