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
import io

def keyword(infilename,outfilename,keywordparam):
    print("Starting: keyword(",infilename,",",outfilename,",",keywordparam,")")

    # Make search case insensitive
    keyword=keywordparam.lower()
    sanitycheck(infilename,outfilename)
    outfile=io.open(outfilename, "w", encoding="utf-8",errors='ignore')

    with io.open(infilename,'r',encoding="utf-8",errors='ignore') as infile:
        for line in infile:

            # Skip empty lines
            if(line.isspace()):
                continue
            try:
                tweet = json.loads(line)

                # In most cases the keyword should be in the 'body' of a tweet,
                if 'body' in tweet:
                    tweetstr=tweet['body'].lower()
                    if(tweetstr.find(keyword) != -1): # if it is found it will return the index, which is greater than 1
                        outfile.write(line)
                        continue
                # but GNIP shortens this body for certain retweets so we also need to check ['object']['body']
                # if it doesn't exist in tweet['body']
                if 'object' in tweet:
                    if 'body' in tweet['object']:
                        tweetstr=tweet['object']['body'].lower()
                        if(tweetstr.find(keyword) != -1):
                            outfile.write(line)
            except:
                print " [ ERROR ] Exception raised"
                print(" [ ERROR ] keyword(",infile,",",outfile,",",keyword,")")
                print("           occurred on line:",line)
                uprint(line)
                error(infilename,outfilename,"Exception in processing tweet")
                raise

    outfile.close()

    

