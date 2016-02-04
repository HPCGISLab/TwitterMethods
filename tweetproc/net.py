#!/usr/bin/python
"""
Copyright (c) 2014 High-Performance Computing and GIS (HPCGIS) Laboratory. All rights reserved.
Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.
Authors and contributors: Eric Shook (eshook@kent.edu);
Website: http://hpcgis.geog.kent.edu
"""

import json
import codecs
from math import *
from tweetproc import *
import csv
import io

def checkcityproximity(citylist,candidate_city,radius):
    #return True
    ll=(candidate_city['lat'],candidate_city['lon']) # Get the latitude and longitude of the candidate city
    for city in citylist:
        d=greatcircledistance( (city['lat'],city['lon']), ll) # Calculate distance
        if d < radius:    # If distance to an existing city is within radius
            return False  # It is too close so return false
    return True # Otherwise if not too close to any existing city, return true

# Removes smaller cities that are too close to larger cities
def removeclosecities(citylist,radius):

    newcitylist=[] # Create a new list for cities
    sortedcitylist = sorted(citylist, key=lambda k: int(k['POP10']),reverse=True) 
    for city in sortedcitylist: # Iterate over sorted cities in the list
        if checkcityproximity(newcitylist,city,radius):
            newcitylist.append(city)
        else:
            print "SKIPPING",city['POP10'],city
    return newcitylist
# Count the number of points in listofpoints that are within the radius to a point at lat,lon coordinates
def countinradius(lat,lon,radius,listofpoints):
    count=0

    for point in listofpoints:
        dist=greatcircledistance((lat,lon),point)
        if(dist<=radius):
            count+=1

    return count


def citydistance(incities,tweets,radius):
   
    cities=incities[:] # Copy the incities list into a new list called cities

    # Loop over the cities
    for index,city in enumerate(incities):

         # Count the number of tweets within the radius to the city (lat,lon) coordinates
         count=countinradius(city['lat'],city['lon'],radius,tweets)
         cities[index]['count']=count

    # Return the new cities list that includes the tweet count for each city
    return cities

# Read the CSV file that contains all the populated places in the US
def processcitycsv(popcutoff):
    filename='data/Gaz_places_national.csv'
    print "Processing city with population cutoff",popcutoff,":",filename
    citylist=[]
    # Read the CSV file
    with open(filename) as csvfile:
        dictreader=csv.DictReader(csvfile)
        for line in dictreader:
            # Convert lat and lon values to what they are called in the code
            line['lat']=float(line['INTPTLAT'])
            line['lon']=float(line['INTPTLONG'])
            try:
                citypop=int(line['POP10'])
                # If the population is above the cutoff, then add the city to citylist
                if citypop >= popcutoff:
                    citylist.append(line)
            except:
                print "[ ERROR ]",line
                raise
    return citylist

def processtweetcsv(infilename,time1,time2):
    print "Processing tweet csv:",infilename
    tweetlist=[]

    with open(infilename) as csvfile:
        dictreader=csv.reader(csvfile)
        for line in dictreader:
            tweettime=dateparser(line[2])
            if time1.date() <= tweettime.date() and tweettime.date() <= time2.date():
                tweetlist.append([float(line[1]),float(line[0])])
    return tweetlist

# Net accepts a geocsv file with a time period defined by time1 and time2
# It outputs a CSV of cities with the number of tweets within distance=radius during the time period (time1-time2)
def net(infilename,time1,time2,minpopulation,radius,incaselocations):

    # First process the geocsv tweet file and remove tweets outside of the time window
    t=processtweetcsv(infilename,time1,time2)
    # Next process the cities and remove cities that are below the minimum population cutoff
    c=processcitycsv(minpopulation)
    # Finally process the case locations (ensure that the locations are floats
    caselocations=[]
    for loc in incaselocations:
        #                    Name    lat           lon
        print loc[0],loc[1],loc[2]
        caselocations.append([loc[0],float(loc[1]),float(loc[2])])


    print "Number of city locations before removing smaller cities",len(c)

    # This function removes smaller cities that are within radius to larger cities
    # Generally this removes suburbs and neighborhoods within large metropolitean areas (e.g., NYC, LA, etc.)
    c=removeclosecities(c,radius)

    print "Number of tweet locations",len(t)
    print "Number of city locations",len(c)
    print "Radius (meters)",radius

    # Calculate NET for each city (c) using list of tweets (t) and distance limit (radius)
    cl=citydistance(c,t,radius)

    # Loop over the cities (c) in the citylist (cl)
    # to calculate the distance to the nearest case location 
    for c in cl:
        mindist=99999999999
        for loc in caselocations: # Loop over case locations
            dist=greatcircledistance((loc[1],loc[2]),(c['lat'],c['lon'])) # Calculate distance
            if(dist<mindist):
               mindist=dist
        c['mindist']=mindist # Only save the shortest (min) distance

    # Now take the results and save the output
    outfilename="csv/out.net-"+str(minpopulation)+"-"+str(radius)+"-"+str(time1.date())+"-"+str(time2.date())+".csv"
    #with io.open(outfilename,'w',encoding="utf-8",errors='ignore') as outfile:
    with open(outfilename,'w') as outfile:
        outfile.write("Population,Tweet Count,Distance to Ebola case,City name,State\n")
        for c in cl:
            outfile.write(str(c['POP10'])+","+str(c['count'])+","+str(int(c['mindist']))+","+c['NAME']+","+c['USPS']+"\n")


