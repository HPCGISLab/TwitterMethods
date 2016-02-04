#!/usr/bin/python
"""
Copyright (c) 2014 High-Performance Computing and GIS (HPCGIS) Laboratory. All rights reserved.
Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.
Authors and contributors: Eric Shook (eshook@kent.edu);
Website: http://hpcgis.geog.kent.edu
"""

'''
import json
from util import *
import io
import re
from .printbody import *
import itertools

wspattern = re.compile(r'\s+')
'''
from datetime import *
from dateutil.parser import parse as dateparser

# Check if a tweet is a retweet
def checkretweet(tweet):

    # Check if tweet is a retweet, indicated by "share" in 'verb'
    if 'verb' in tweet and tweet['verb'] == "share":
        return True
 
    # Extract out the tweet text, use the object body if it exists, because retweets are shortened in tweet['body']
    # so if tweet['object']['body'] is available we will use that first
    tweetstr=""
    if 'object' in tweet and 'body' in tweet['object']:
        tweetstr=tweet['object']['body'].lower()
    elif 'body' in tweet:
        tweetstr=tweet['body'].lower()
    else:
        return False # If no tweet text, then return false because there was no match

    # This second check looks for 'unofficial' tweets that retweet without officially marking it as a retweet in Twitter
    # It is common for people to copy/paste a tweet and add RT in the 
    if 'rt @' in tweetstr or 'rt@' in tweetstr:
        return True

    return False

# Check if tweet was tweeted during a time window (time1-time2), which are normalized to EST
def checktime(tweet,time1,time2):
    # Get the time this tweet was tweeted
    if "postedTime" in tweet:
        tweettime=tweet['postedTime']
        tweettime=dateparser(tweettime) # Get the date
        td=timedelta(hours=-5) # Normalize times to EST (-5 hours to GMT as reported from GNIP)
        tweettime+=td # Add the time delta to tweet time to get time of tweet in EST 

        # If tweet time is between or the same as time1 and time2 then it is good
        if time1.date() <= tweettime.date() and tweettime.date() <= time2.date():
            return True
    return False

