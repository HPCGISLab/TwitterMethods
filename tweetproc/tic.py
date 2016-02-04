#!/usr/bin/python
"""
Copyright (c) 2014 High-Performance Computing and GIS (HPCGIS) Laboratory. All rights reserved.
Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.
Authors and contributors: Eric Shook (eshook@kent.edu);
Website: http://hpcgis.geog.kent.edu
"""

import json
#import codecs
import io
from dateutil.parser import parse as dateparser
from .priskproxy import *
from .tweetutil import *
from .util import *

# Tweet-based measure of Immediate Concern
# counts the number of tweets for each user within a single time period
def tic(infilename,time1,time2):

    # Create an empty dictionary that will store userid and the number of their tweets
    users={}

    # Sanity check uses a fake file as the output, since this method does not write to an output file
    # Instead it returns a dictionary of users (key) and their tweet count (value)
    sanitycheck(infilename,"/tmp/tmp.1234.tmp.tweetproc")
    with io.open(infilename,'r',encoding="utf-8",errors='ignore') as infile:
        for line in infile:
            if(line.isspace()): # Skip empty lines
                continue
            try:
                tweet = json.loads(line) # Try to load the json line

                # Do not count retweets as they are not original posts
		if checkretweet(tweet): 
		    continue

                # Only allow tweets within the timeline
		if not checktime(tweet,time1,time2):
		    continue

                # Use the userid to count the number of tweets (or in GNIP terms actor id)
                if "actor" in tweet and "id" in tweet['actor']:
                    userid=tweet['actor']['id']

                    # Increment by 1 by default, since the user posted this tweet
                    inc=1
                    #if(checkconcern(tweet)): # If it is a concerned tweet let it count as two tweets
                    #    inc+=1               # This is used as an adapted method to the original TIC

                    if userid in users:
                        users[userid]+=inc
                    else:
                        users[userid]=inc
            except:
                print " [ ERROR ] Exception raised"
                print(" [ ERROR ] users(",infilename,")")
                print("           occurred on line:",line)
                uprint(line)
                raise

    return users 

