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

def geo(infilename,outfilename):
    print("Starting: geo(",infilename,",",outfilename,")")

    sanitycheck(infilename,outfilename)
    outfile=io.open(outfilename, "w", encoding="utf-8",errors='ignore')

    with io.open(infilename,'r',encoding="utf-8",errors='ignore') as infile:
        for line in infile:

            # Skip empty lines
            if(line.isspace()):
                continue
            try:
                tweet = json.loads(line)

                # Check existence of multiple geo tags in a tweet or retweet
	        if "object" in tweet and "geo" in tweet["object"]: 
		    outfile.write(line)
                    continue

                if "object" in tweet and "location" in tweet["object"]: 
                    outfile.write(line)
                    continue

                if "geo" in tweet:
                    outfile.write(line)
                    continue

                if "location" in tweet:
                    outfile.write(line)
                    continue

            except:
                print " [ ERROR ] Exception raised"
                print(" [ ERROR ] geo(",infilename,",",outfilename,")")
                print("           occurred on line:",line)
                uprint(line)
                error(infilename,outfilename,"Exception in processing tweet")
                raise

    outfile.close()

    

