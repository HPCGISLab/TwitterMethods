#!/usr/bin/python

import tweetproc 
'''
import os
from multiprocessing import Pool
import copy
'''

# Radius in meters for case locations
#caseradius=100000

# Radius in meters for campus locations
#campusradius=15000
#campusradius=25000

# List of sites that will be investigated including the search radius
'''
sites=[
 #Sitename    #Latitude  #Longitude  #Radius (meters)
#["Ohio",      41.071312, -81.400874, caseradius], # Stonegate Trail, Tallmadge, OH (Development where Amber Vinson stayed while in Ohio)
#["Texas",     32.881525, -96.762410, caseradius], # Texas Health Presbyterian Hospital Dallas, 8200 Walnut Hill Lane, Dallas, TX 75231
#["NewYork",   40.738766, -73.975368, caseradius], # Bellevue Hospital Center, 462 1st Avenue, New York, NY 10016
["Tuscarawas",40.467441, -81.407072, campusradius],
["Salem",     40.864983, -80.835811, campusradius],
["Trumbull",  41.279297, -80.838332, campusradius],
["Ashtabula", 41.889173, -80.831944, campusradius],
["ELiverpool",40.617236, -80.576320, campusradius],
["Geauga",    41.509121, -81.150659, campusradius],
["Stark",     40.866924, -81.436568, campusradius],
["Kent",      41.149326, -81.341411, campusradius]
]

sites=[
["THPHDallas",      32.881525, -96.762410, campusradius], # Texas Health Presbyterian Hospital Dallas, 8200 Walnut Hill Lane, Dallas, TX 75231 (duplicate)
#["THPHAllen",       33.116341, -96.673193, campusradius], # Texas Health Presbyterian Hospital Allen 1105 Central Expressway Allen, TX 75013 
#["THPHDenton",      33.217850, -97.166504, campusradius], # Texas Health Presbyterian Hospital Denton 3000 North I-35 Denton, TX 76201 
#["THPHKaufman",     32.591426, -96.318062, campusradius], # Texas Health Presbyterian Hospital Kaufman 850 Ed Hall Drive Kaufman, TX 75142 
#["THPHPlano",       33.044414, -96.835895, campusradius], # Texas Health Presbyterian Hospital Plano 6200 West Parker Road Plano, TX 75093 
#["THPHFlowerMound", 33.045827, -97.067547, campusradius], # Texas Health Presbyterian Hospital Flower Mound 4400 Long Prairie Road Flower Mound, TX 75028 
#["THPHRockwall",    32.884425, -96.466031, campusradius], # Texas Health Presbyterian Hospital Rockwall 3150 Horizon Road Rockwall, TX 75032 
]
'''


siteiter=-1 # Global variable to identify a site in the sites list
radius=-1   # Global variable to set search radius for a site
sites=None



def runsites(siteslist):
    global sites
    global radius
    global siteiter

    # Set the global variable
    sites=siteslist

    # Loop over each site
    for i in xrange(len(sites)):
        siteiter=i 
        radius=sites[siteiter][3]
        print "Processing",sites[siteiter][0],"radius",radius
        inputdir= "data/geoebola"
        outputdir="data/geoebola-sites-"+sites[siteiter][0]+"-"+str(radius)

        tweetproc.process(runit,inputdir,outputdir,12)

# Extract latitude and longitude coordinates and search radius from each site
# Run georadius method that saves tweets within radius of site location
def runit(params):
    plist=list(params)
    plist.append(sites[siteiter][1])
    plist.append(sites[siteiter][2])
    plist.append(radius)
    tweetproc.georadius(*plist)

# Run the case sites data 
#sites=tweetproc.casesites
runsites(tweetproc.casesites)

