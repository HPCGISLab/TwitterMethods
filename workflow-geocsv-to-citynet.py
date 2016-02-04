#!/usr/bin/python
"""
Copyright (c) 2014 High-Performance Computing and GIS (HPCGIS) Laboratory. All rights reserved.
Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.
Authors and contributors: Eric Shook (eshook@kent.edu);
Website: http://hpcgis.geog.kent.edu
"""

import json
import codecs
import random
from math import *
from tweetproc import *
import csv

# Radius to city location (meters)
radius=15000
radius=100000
radius=50000

# Minimum city population to calculate
minpopulation=500000
minpopulation=100000

# Geocsv input file
infilename="csv/out.geoebola.csv"

# Calculate NET for each US-diagnosed Ebola case
#net(infilename,tdtime1,tdtime2,minpopulation,radius,[casesites[1]]) # [1]=Texas
net(infilename,nptime1,nptime2,minpopulation,radius,[casesites[1]]) # [1]=Texas
#net(infilename,avtime1,avtime2,minpopulation,radius,[casesites[0],casesites[1]]) # [0]=Ohio,[1]=Texas
#net(infilename,cstime1,cstime2,minpopulation,radius,[casesites[2]]) # [2]=NewYork

