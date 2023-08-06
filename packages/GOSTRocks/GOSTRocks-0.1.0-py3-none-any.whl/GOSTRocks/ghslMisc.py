import sys, os, inspect, logging, json
import rasterio, affine, pyproj

import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray as rxr

from matplotlib.colors import ListedColormap, BoundaryNorm
from collections import Counter
from shapely.geometry import box
from shapely import wkt
from affine import Affine
from rasterio import features
from rasterio.mask import mask
from rasterio.features import rasterize, MergeAlg
from rasterio.warp import reproject, Resampling
from rasterio import MemoryFile
from contextlib import contextmanager

curPath = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if not curPath in sys.path:
    sys.path.append(curPath)

from misc import tPrint
import rasterMisc as rMisc

def calculate_ghsl_categorical(ghsl_folder, out_file):
    ''' Combine the individual ghsl_files into a single raster where pixels identify the year built
    '''
