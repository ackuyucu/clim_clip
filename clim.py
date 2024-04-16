#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
from osgeo import gdal
import sys
import os
import subprocess

# If sys.argv[3,4 and 5] are not defined, the script will run with the default values
# If sys.argv[3,4 and 5] are defined, the script will run with the values defined by the user
# The default values are: proj = "EPSG:4326", oubound = (-20, 20, 60, 60), res = 0.041666666666667

def main(dirpath, contpathfile, proj = "EPSG:4326", outbound = (-20, 20, 65, 65), res = 0.041666666666667):  # WORK on implementing the arguments
    # Define all the files in the folder as a list named tifs
    pathini = sys.argv[1]
    continents = sys.argv[2]
    tifs = glob.glob(os.path.join(pathini, "*.tif"))                        
    print(tifs)

    # For loop to reproject, crop and rename appropriate to maxent for all the files in the list
    for tif in tifs:
        # Open the file
        ds = gdal.Open(tif)
        # Define the output file name
        out = tif[:-4] + "_reprojected.tif"
        # Define the output projection
        # The default projection is WGS84 (EPSG:4326)
        # The projection can be changed by the user in the input arguments
        if len(sys.argv) > 3:
            proj = sys.argv[3]
        else:
            proj = "EPSG:4326"
        # Define boundaries of the output file
        # The boundaries are defined by the coordinates of the lower left and upper right corners
        # The coordinates are in the order of (minX, minY, maxX, maxY) default is (-20, 20, 60, 60)
        # The boundaries can be changed by the user in the input arguments
        if len(sys.argv) > 4:
            # Take arguments from the command line and convert them to a tuple
            outbound = tuple(map(float, sys.argv[4].split(",")))
        else:
            oubound = (-20, 20, 65, 65)
        # Define the output resolution for x and y
        # For this, output resolution is equal to 2.5 arc minutes as default
        # The resolution can be changed by the user in the input arguments
        if len(sys.argv) >= 5:
            res = float(sys.argv[5])
        else:
            res = float(0.041666666666667)
        resx = res
        resy = -1 * res
        # Reproject and resample the file
        gdal.Warp(out, ds, dstSRS=proj, outputBounds=outbound, xRes=resx, yRes=resy)
        # Crop the file using the boundaries of the continents
        out2 = tif[:-4] + "_reprojected_cropped.tif"

        gdal.Warp(out2, out, cutlineDSName=continents, cropToCutline=True, dstNodata = -9999, outputType=gdal.GDT_Float32)


        os.remove(out)
        os.remove(tif)






main(*sys.argv[1:])



