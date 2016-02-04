#!/usr/bin/python
"""
Copyright (c) 2014 High-Performance Computing and GIS (HPCGIS) Laboratory. All rights reserved.
Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.
Authors and contributors: Eric Shook (eshook@kent.edu);
Website: http://hpcgis.geog.kent.edu
"""


import json
from .util import *
from .tweetutil import *
import io
import itertools
'''
from dateutil.parser import parse as dateparser
from datetime import *
#from .printbody import *
'''
import re

wspattern = re.compile(r'\s+')

# This function checks a tweet line against an array of conditions
def priskproxycomplex(tweet,checkarray,modifiers):
    # Extract out the tweet text, use the object body if it exists, because retweets are shortened in tweet['body']
    # so if tweet['object']['body'] is available we will use that first
    tweetstr=""
    if 'object' in tweet and 'body' in tweet['object']:
        tweetstr=tweet['object']['body'].lower()
    elif 'body' in tweet:
        tweetstr=tweet['body'].lower()
    else:
        return False # If no tweet text, then return false because there was no match

    # This is a regular expression pattern for white space
    tweetstr = re.sub(wspattern,' ',tweetstr) # Replace all white space with a single space, helps clean up string for string search

    # Check each proxy strings in the check list
    for proxystr in checkarray:
        if proxystr in tweetstr: # Python substring search for the proxy string
            # Now we must check if it matches the array + modifier
            testmodifier=True
            for modifier in modifiers: # If there is a modifer such as "not" then we must make sure it does not match the modifier
                modifiedproxystr=modifier+" "+proxystr
                #print 'modified proxy str',modifiedproxystr,'tweet text',tweetstr
                if modifiedproxystr in tweetstr: # It matches so this is a false positive
                    #print 'MATCH : modified proxy str',modifiedproxystr,'tweet text',tweetstr
                    testmodifier=False           # Mark it as false 
            if testmodifier:
                # Passed the modifier test as well            
                return True
    return False 

# This function checks a tweet line against an array of conditions
# This function is the simple version of complex
def priskproxy(tweet,checkarray):
    # Extract out the tweet text, use the object body if it exists, because retweets are shortened in tweet['body']
    # so if tweet['object']['body'] is available we will use that first
    tweetstr=""
    if 'object' in tweet and 'body' in tweet['object']:
        tweetstr=tweet['object']['body'].lower()
    elif 'body' in tweet:
        tweetstr=tweet['body'].lower()
    else:
        return False # If no tweet text, then return false because there was no match

    # This is a regular expression pattern for white space
    tweetstr = re.sub(wspattern,' ',tweetstr) # Replace all white space with a single space, helps clean up string for string search

    # Check each proxy strings in the check list
    for proxystr in checkarray:
        if proxystr in tweetstr: # Python substring search
            #print tweetstr
            return True
    return False 

# The following code is not commented as it is repeats
# Each check uses a set of keywords adapted from: 
# If necessary the code also checks a set of modifiers that often negate a phrase to eliminate false positive matches
# The bottom code uses the same technique except finding matches with Ebola and behavior response including hand washing, hand sanitizing, and avoiding people

def checkconcernforothers(tweet):
    # Concern for others
    concernforothers=["hope you don't get","hope you're not sick","hope you aren't sick","hope u don't get","hope u aren't infected","hope you aren't infected","get better","get well","take care","are you ok","is it ebola","is it the ebola","r u ok","hope he is ok","hope she is ok","hope u r ok","go to the doctor","go to the clinic","get checked out","get tested","quarantine yourself","stay home","poor "]

    return priskproxy(tweet,concernforothers)

# Check concern is slightly modified from the publication, because we remove concern for others from this check
# Concern for others is different than personal perceived risk, which is what we are creating a tweet-based measure for
def checkconcern(tweet):

    if(checkconcernforothers(tweet)):
        return True

    concernforself=["i might have ebola","i might have the ebola","i think i have the ebola","i think i have ebola","i don't want to die","i have a fever","i have symptoms","i feel sick","not feeling well","feeling sick","i'm sick"]

    if(priskproxy(tweet,concernforself)):
        return True

    concernedemoticons=[":(",":-(",":'(","='(",":\\","=|",":|",":o","o.o",":s"]

    if(priskproxy(tweet,concernedemoticons)):
        return True

    concerngeneralsimple=["confused","confusing","yikes","uneasy","grief","less deadly","dread","stay away","stay tf away"]

    if(priskproxy(tweet,concerngeneralsimple)):
        return True

    modifiers=["not","dont be","don't be","stop","stop being","quit"]

    concerngeneralcomplex=["worried","worry","scared","scary","frightened","dangerous","freaking out","freakin out","sad","stress","worrisome","freaking me out","freakin me out","nervous","terrified","uneasy"]

    if(priskproxycomplex(tweet,concerngeneralcomplex,modifiers)):
        return True
    
    other=["getting real","gettin real","ebola is in","ebola is here","ebola was at","ebola is at"]

    if(priskproxy(tweet,other)):
        return True

    return False

def checkfrustration(tweet):
    frustrationlist=["ebola sucks","grr","wtf","annoy","irritat","pathetic","pissed","freakin ebola","fml","fuck","shit",":@",":|",":(","shutup","friggin","getting out of hand","stupid","hate ebola","hate being sick","hate it","ebola sucks","damn","effing","freaking ebola","frick","i can't believe","they better not","i am mad","i'm mad ","im mad ","is mad ","so mad ","frustrated","angry","outrage","cranky","peeved","furious","bitter"," irk","crushed","so sick of","if i hear"]

    if(priskproxy(tweet,frustrationlist)):
       return True
    return False

def checksarcasm(tweet):
    sarcasmlist=["lol","lmao","haha","hehe","hilarious","funny","j/k"," xd ",":p","=p","rofl",":)","=)"," jk "," xp ",";)","=d",":d","ha ha","just kiddin","he he","heh", "still a thing"]

    if(priskproxy(tweet,sarcasmlist)):
       return True

    modifiers=["not","dont be","don't be","stop","stop being","quit","not a"]
    sarcasmcomplex=["joke","joking"]

    if(priskproxycomplex(tweet,sarcasmcomplex,modifiers)):
        return True

    return False

def checkdownplay(tweet):
    downplaylist=["not a big deal","hype","overblown","just ebola","not worried","not afraid","it's not that bad","i've had worse","hysteria","just relax","calm down","don't panic","not concerned","what's the big deal","not dangerous","less dangerous","less deadly","more people die from","million people have aids","don't care","not worried","dont care","who cares","ebola is nothing"]

    if(priskproxy(tweet,downplaylist)):
       return True

    modifiers=["dont","don't","do not","won't","will not"]
    forgetcomplex=["forget ebola","forget about ebola"]

    if(priskproxycomplex(tweet,forgetcomplex,modifiers)):
        return True

    modifiers=["i am","im","i'm","i'm getting","im getting","i am","i'm becoming","i am becoming","im becoming","i am so","i'm so","im so"]
    paranoidcomplex=["paranoi"]
    if(priskproxycomplex(tweet,paranoidcomplex,modifiers)):
        return True

    return False

def checkindirectexperience(tweet):
    indirectexperiencelist=["my mom","my mum","my mother","my dad","my father","my bro","my sis","my uncle","my aunt","my grandm","my grandpa","my grandfather","my cousin","my niece","my nephew","my friend","my classmate","my neighbor","my roommate","my boyfriend","my girlfriend","my bf","my gf","my wife","my husband","my kid","my son","my daughter","my baby","my doctor","my co-worker","my coworker","my co worker","my class","my school","my university","my church","my city","my town","my dorm","my rez","my campus","my home","my house","my office","my work","my country","my state"]

    return priskproxy(tweet,indirectexperiencelist)

def checkexperience(tweet):

    pexperiencelist=["getting tested for ebola","getting checked out for ebola","going to the doctor","went to the doctor","going to see the doctor","went to the clinic","went to a clinic","going to the clinic","going to a clinic","i'm getting sick","im getting sick","i have symptoms","i have a fever","i'm feeling sick"]

    if(priskproxy(tweet,pexperiencelist)):
       return True

    if(checkindirectexperience(tweet)):
       return True

    return False

def checkopinion(tweet):
    opinionlist=["in my opinion","love","i think","imho","government should","gov't should","doctors should","obama should","media should","cdc should","i believe","schools should","teachers should","hospitals should","people should","my stance","my take","my view","my feeling","my impression","my theory","my thought"," pov ","my opinion","i recommend","i suggest","my suggestion","did you hear","reading","interest","researching","heard ","i read","i hear","i feel that"]

    if(priskproxy(tweet,opinionlist)):
       return True

    lookinguplist=["looking up"]
    modifiers=["things are","it's"]
    if(priskproxycomplex(tweet,lookinguplist,modifiers)):
        return True

    tweetstr=""
    if 'object' in tweet and 'body' in tweet['object']:
        tweetstr=tweet['object']['body'].lower()
    elif 'body' in tweet:
        tweetstr=tweet['body'].lower()
    else:
        return False # If no tweet text, then return false because there was no match

    # Custom complex checks from SQL queries
    if 'read ' in tweetstr and not 'spread ' in tweetstr:
        return True
    if 'reading ' in tweetstr and not 'spreading ' in tweetstr:
        return True
    return False

def checkrelief(tweet):

    relieflist=["relieved","thank god","thankful","whew","i am ok","im ok","i'm ok","all better","relief","i'm recovering","i just recovered","i've recovered","back at school","back at work","happy to hear","glad to hear","i'm safe","good to hear","happy that","good that","survived","bounced back","recuperate","escape"]

    if(priskproxy(tweet,relieflist)):
       return True

    reliefcomplex=["feeling better"]
    modifiers=["not"]
    if(priskproxycomplex(tweet,reliefcomplex,modifiers)):
        return True

    return False

def checkquestion(tweet):
    questionmark=["?"]

    if(priskproxy(tweet,questionmark)):
       return True
    return False

# If a URL was provided
def checkresource(tweet):
    if 'twitter_entities' in tweet and 'urls' in tweet['twitter_entities']:
        if len(tweet['twitter_entities']['urls'])>0:
            return True
    return False


def checkhandwash(tweet):
    bresponselist=["wash your hand","wash my hand","wash hand","wash yer hand","wash yo hand","washing my hand","washing your hand","hand wash","handwash","washhand","wash your damn hands","wash your fucking hand","wash your freakin hand","wash your freaking hand","soap"]

    if(priskproxy(tweet,bresponselist)):
       return True
    return False


def checksanitize(tweet):
    bresponselist=["sanitize your hand","sanitize my hand","sanitize hand","sanitize yer hand","sanitize yo hand","sanitizeing my hand","sanitizeing your hand","hand sanitize","handsanitize","sanitizehand","sanitize your damn hands","sanitize your fucking hand","sanitize your freakin hand","sanitize your freaking hand"]

    if(priskproxy(tweet,bresponselist)):
       return True
    return False


def checkcough(tweet):

    # Try various combinations of coughing and "near me's"
    first=["cough","coughs","coughing","sneeze","sneezes","sneezing"]
    second=["in my direction","on me","next to me","near me","by me"]
    stringlist=[' '.join(x) for x in itertools.product(first,second)]
    if(priskproxy(tweet,stringlist)):
       return True
    return False

def checkavoidgathering(tweet):
    bresponselist=["stay away","keep away","not leaving","stay tf away","keep tf away","keep away","keep tf away","don't get close","dont get close","i'm leaving","i left","running away","run away","nobody come over","don't touch me","dont touch me","stays home","staying home","i'm moving","keep the fuck away","stay the fuck away"]

    if(priskproxy(tweet,bresponselist)):
       return True
    return False


def checkavoidschool(tweet):
    bresponselist=["skipping class","skipping school","skip class","not going to class","aint going to class","cancel class","close university","close the university","call of work","skip work","skipping work","not going to work","aint going to work","shut down campus","shutdown campus"]

    if(priskproxy(tweet,bresponselist)):
       return True
    return False


#This function codes tweets based on a series of categories 
def tweetcoding(infilename,time1,time2):

    # Create an empty user dictionary, which will be returned at the end of the function
    users={}

    # Sanity check does not need to look for an output file since the results are returned
    sanitycheck(infilename,"/tmp/tmp.1234.tmp.tweetproc")
    with io.open(infilename,'r',encoding="utf-8",errors='ignore') as infile:
        for line in infile:
            if(line.isspace()): # Skip spaces
                continue
            try:
                tweet = json.loads(line)
                if(checkretweet(tweet)): # Skip retweets
                    continue
                if(not checktime(tweet,time1,time2)): # Skip tweets outside of time window
                    continue

                tweetcoding={'concern':0,
                 'experience':0,
                 'opinion':0,
                 'sarcasm':0,
                 'relief':0,
                 'downplay':0,
                 'frustration':0,
                 'total':0
                }


                if(checkconcern(tweet)):
                    tweetcoding['concern']+=1
                if(checkexperience(tweet)):
                    tweetcoding['experience']+=1
                if(checkopinion(tweet)):
                    tweetcoding['opinion']+=1
                if(checksarcasm(tweet)):
                    tweetcoding['sarcasm']+=1
                if(checkrelief(tweet)):
                    tweetcoding['relief']+=1
                if(checkdownplay(tweet)):
                    tweetcoding['downplay']+=1
                if(checkfrustration(tweet)):
                    tweetcoding['frustration']+=1
                tweetcoding['total']+=1
               
                # Add this coded tweet for the user that posted it 
                if "actor" in tweet and "id" in tweet['actor']:
                    userid=tweet['actor']['id']

                    if userid in users: # If user is already in the list
                        for br in tweetcoding: # Loop over each behavior response
                            users[userid][br]+=tweetcoding[br] # Add the value from this tweet
                    else:
                        users[userid]=tweetcoding
 
            except:
                print " [ ERROR ] Exception raised"
                print(" [ ERROR ] tweetcoding(",infilename,")")
                print("           occurred on line:",line)
                uprint(line)
                error(infilename,None,"Exception in processing tweet")
                raise

    return users 

#This function codes tweets searching for behavior responses 
def tweetcodingbresponse(infilename,time1,time2):

    # Create an empty user dictionary, which will be returned at the end of the function
    users={}


    # Sanity check does not need to look for an output file since the results are returned
    sanitycheck(infilename,"/tmp/tmp.1234.tmp.tweetproc")
    with io.open(infilename,'r',encoding="utf-8",errors='ignore') as infile:
        for line in infile:
            if(line.isspace()): # Skip empty lines
                continue
            try:
                tweet = json.loads(line)
                if(checkretweet(tweet)): # Skip retweets
                    continue
                if(not checktime(tweet,time1,time2)): # Skip tweets outside of time window
                    continue

                # Set a generic template for all behavior responses
                tweetcoding={'handwash':0,
                 'handsanitize':0,
                 'cough':0,
                 'avoidgathering':0,
                 'avoidschool':0,
                 'total':0
                }

                # Check each behavior response and increase the value if it is recognized
                if(checkhandwash(tweet)):
                    tweetcoding['handwash']+=1
                if(checksanitize(tweet)):
                    tweetcoding['handsanitize']+=1
                if(checkcough(tweet)):
                    tweetcoding['cough']+=1
                if(checkavoidgathering(tweet)):
                    tweetcoding['avoidgathering']+=1
                if(checkavoidschool(tweet)):
                    tweetcoding['avoidschool']+=1
                tweetcoding['total']+=1

                # Add this coded tweet for the user that posted it 
                if "actor" in tweet and "id" in tweet['actor']:
                    userid=tweet['actor']['id']

                    if userid in users: # If user is already in the list
                        for br in tweetcoding: # Loop over each behavior response
                            users[userid][br]+=tweetcoding[br] # Add the value from this tweet
                    else:
                        users[userid]=tweetcoding
                
                
            except:
                print " [ ERROR ] Exception raised"
                print(" [ ERROR ] tweetcodingbresponse(",infilename,")")
                print("           occurred on line:",line)
                uprint(line)
                raise
                error(infilename,None,"Exception in processing tweet")

    return users 



