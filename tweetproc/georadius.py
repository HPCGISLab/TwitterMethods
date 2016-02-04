#!/usr/bin/python
"""
Copyright (c) 2014 High-Performance Computing and GIS (HPCGIS) Laboratory. All rights reserved.
Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.
Authors and contributors: Eric Shook (eshook@kent.edu);
Website: http://hpcgis.geog.kent.edu
"""

import json
#import codecs
from util import *
from math import *
import io

# Extract out location information from tweets and test whether the location is within radiusm of the coordinate (lat,lon)
def handlegeoradius(geo,lat,lon,radiusm):
        if(geo==None): # If no geospatial information is present, then it cannot match
            return False 
        if(geo['type']=="Point"): # Point is the simple case
	    testlat=geo['coordinates'][0]
            testlon=geo['coordinates'][1]
            #print "POINT testlat",testlat,"testlon",testlon
        elif(geo['type']=="Polygon"): # Polygon is the complex case
            coordinates=geo['coordinates']
            # Sanity check polygon is only a bounding box (4 corner coordinates)
            if(len(coordinates)!=1 or len(coordinates[0])!=4): 
                error("polygon size is not correct")
            coordinates=coordinates[0] # Extract the simple polygon
            # Zip takes the four coordinate pairs and puts them into a list of latitudes and longitudes 
            # Specifically, [ [,] [,] [,] [,] to [ [, , , ] [, , , ] ]
            lllist=zip(coordinates[0],coordinates[1],coordinates[2],coordinates[3]) 
            #Central location for point, which is the sum of lats and then lons divided by the number (4)
            testlat=sum(lllist[1])/float(len(lllist[1]))
            testlon=sum(lllist[0])/float(len(lllist[0]))
            #print "POLYG testlat",testlat,"testlon",testlon
        # Distance check between lat,lon (point passed in) and testlat,testlon (tweet location) using radiusm
	dist=greatcircledistance((lat,lon),(testlat,testlon))
        #print "dist=",dist
        #print "radiusm=",radiusm
        #print "lat",lat,"lon",lon
        #print "testlat",testlat,"testlon",testlon
        if(dist>radiusm):
            return False
        else:
            return True

# Test tweets to see if they are within the radius
def georadius(infilename,outfilename,lat,lon,radiusm):
    print("Starting: georadius(",infilename,",",outfilename,",",lat,",",lon,",",radiusm,")")

    sanitycheck(infilename,outfilename)
    outfile=io.open(outfilename, "w", encoding="utf-8",errors='ignore')
    with io.open(infilename,'r',encoding="utf-8",errors='ignore') as infile:
        for line in infile:
            if(line.isspace()):
                continue
            try:
                tweet = json.loads(line)
                # Check existence of multiple geo tags in a tweet
                # We remove state location matches as they are too coarse.
	        if "object" in tweet and "geo" in tweet["object"]: 
		    geo=tweet['object']['geo']
                    if(handlegeoradius(geo,lat,lon,radiusm)):
		        outfile.write(line)
                        continue

                if "object" in tweet and "location" in tweet["object"]: 
                    if ", US" in tweet['object']['location']['displayName']: # If it matches a State by <State name>, US
                        continue                                             # Then skip it
		    geo=tweet['object']['location']['geo']
                    if(handlegeoradius(geo,lat,lon,radiusm)):
		        outfile.write(line)
                        continue

                if "geo" in tweet:
                    geo=tweet['geo']
                    if(handlegeoradius(geo,lat,lon,radiusm)):
		        outfile.write(line)
                        continue

                if "location" in tweet:
                    if ", US" in tweet['location']['displayName']:           # If it matches a State by <State name>, US
                        continue                                             # Then skip it
                    geo=tweet['location']['geo']
                    if(handlegeoradius(geo,lat,lon,radiusm)):
		        outfile.write(line)
                        continue
            except:
                print " [ ERROR ] Exception raised"
                print(" [ ERROR ] georadius(",infile,",",outfile,")")
                print("           occurred on line:",line)
                uprint(line)
                error(infilename,outfilename,"Exception in processing tweet")
                raise

    outfile.close()
    checkandremoveemptyfile(outfilename)
    

