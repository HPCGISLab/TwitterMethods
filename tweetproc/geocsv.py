#!/usr/bin/python
"""
Copyright (c) 2014 High-Performance Computing and GIS (HPCGIS) Laboratory. All rights reserved.
Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.
Authors and contributors: Eric Shook (eshook@kent.edu);
Website: http://hpcgis.geog.kent.edu
"""

import json
import codecs
from util import *
import io
from dateutil.parser import parse as dateparser
import re
from datetime import *

wspattern = re.compile(r'\s+')

def handlegeocsv(geo,tweet):
        if(geo==None):
            return ""

        tweettime=""
        tweetuser=""
        bodytext=""
        if "postedTime" in tweet:
            tweettime=tweet['postedTime']
            tweettime=dateparser(tweettime) # Get the date
            td=timedelta(hours=-5) # Normalize times to EST (-5 hours to GMT as reported from GNIP)
            tweettime+=td # Add the time delta to tweet time to get time of tweet in EST 
            tweettime=tweettime.strftime("%Y%m%d")
        if "actor" in tweet and "displayName" in tweet['actor']:
            tweetuser=tweet['actor']['displayName']
        if "body" in tweet:
            bodytext=tweet['body']
            #bodytext = re.sub(wspattern,' ',bodytext)
	#endstr=","+tweettime+","+tweetuser+","+bodytext
	endstr=","+tweettime

        if(geo['type']=="Point"):
            lat=str(geo['coordinates'][1])
            lon=str(geo['coordinates'][0])
            return lat.decode('utf-8')+","+lon.decode('utf-8')+endstr+"\n"
        elif(geo['type']=="Polygon"):
            coordinates=geo['coordinates']
            # Sanity check polygon is simple (only a bounding box)
            if(len(coordinates)!=1 or len(coordinates[0])!=4):
                error("polygon size is not correct")
            coordinates=coordinates[0] # Enter the simple polygon
            lllist=zip(coordinates[0],coordinates[1],coordinates[2],coordinates[3])
            lonavg=sum(lllist[0])/float(len(lllist[0]))
            latavg=sum(lllist[1])/float(len(lllist[1]))
            return str(round(lonavg,5)).decode('utf-8')+","+str(round(latavg,5)).decode('utf-8')+endstr+"\n"
        else:
            return ""
        

def geocsv(infilename):

    # Start with an empty string
    outputstring=""

    sanitycheck(infilename,"/tmp/out.tmp.12345")
    with io.open(infilename,'r',encoding="utf-8",errors='ignore') as infile:
        for line in infile:
            if(line.isspace()): # Skip empty lines
                continue
            try:
                tweet = json.loads(line)
                # Check existence of multiple geo tags in a tweet
                if "geo" in tweet:
                    geo=tweet['geo']
                    outputstring+=handlegeocsv(geo,tweet)
                    continue

                if "location" in tweet:
                    if ", US" in tweet['location']['displayName']:           # If it matches a State by <State name>, US
                        continue                                             # Then skip it
                    geo=tweet['location']['geo']
                    outputstring+=handlegeocsv(geo,tweet)
                    continue

	        if "object" in tweet and "geo" in tweet["object"]: 
		    geo=tweet['object']['geo']
                    outputstring+=handlegeocsv(geo,tweet)
                    continue

                if "object" in tweet and "location" in tweet["object"]: 
                    if ", US" in tweet['object']['location']['displayName']: # If it matches a State by <State name>, US
                        continue                                             # Then skip it
		    geo=tweet['object']['location']['geo']
                    outputstring+=handlegeocsv(geo,tweet)
                    continue

            except:
                print " [ ERROR ] Exception raised",sys.exc_info()[0]
                print(" [ ERROR ] geocsv(",infilename,")")
                print("           occurred on line:",line)
                raise
                error(infilename,outfilename,"Exception in processing tweet")

    return outputstring
    

