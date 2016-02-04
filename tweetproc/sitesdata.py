#!/usr/bin/python

from datetime import *

# Case radius in meters
caseradius=100000
caseradius=50000

# Campus radius in meters
campusradius=15000
campusradius=25000

# US-Ebola case locations before diagnosis 
casesites=[
#Sitename    #Latitude  #Longitude  #Radius (meters)
["Ohio",      41.071312, -81.400874, caseradius], # Stonegate Trail, Tallmadge, OH (Development where Amber Vinson stayed while in Ohio)
["Texas",     32.881525, -96.762410, caseradius], # Texas Health Presbyterian Hospital Dallas, 8200 Walnut Hill Lane, Dallas, TX 75231
["NewYork",   40.738766, -73.975368, caseradius]  # Bellevue Hospital Center, 462 1st Avenue, New York, NY 10016
]

# Kent Campus locations
campussites=[
["Tuscarawas",40.467441, -81.407072, campusradius],
["Salem",     40.864983, -80.835811, campusradius],
["Trumbull",  41.279297, -80.838332, campusradius],
["Ashtabula", 41.889173, -80.831944, campusradius],
["ELiverpool",40.617236, -80.576320, campusradius],
["Geauga",    41.509121, -81.150659, campusradius],
["Stark",     40.866924, -81.436568, campusradius],
["Kent",      41.149326, -81.341411, campusradius]
]

# Texas Health Presbyterian Hospital locations
texassites=[
["THPHDallas",      32.881525, -96.762410, campusradius], # Texas Health Presbyterian Hospital Dallas, 8200 Walnut Hill Lane, Dallas, TX 75231 (duplicate)
["THPHAllen",       33.116341, -96.673193, campusradius], # Texas Health Presbyterian Hospital Allen 1105 Central Expressway Allen, TX 75013 
["THPHDenton",      33.217850, -97.166504, campusradius], # Texas Health Presbyterian Hospital Denton 3000 North I-35 Denton, TX 76201 
["THPHKaufman",     32.591426, -96.318062, campusradius], # Texas Health Presbyterian Hospital Kaufman 850 Ed Hall Drive Kaufman, TX 75142 
["THPHPlano",       33.044414, -96.835895, campusradius], # Texas Health Presbyterian Hospital Plano 6200 West Parker Road Plano, TX 75093 
["THPHFlowerMound", 33.045827, -97.067547, campusradius], # Texas Health Presbyterian Hospital Flower Mound 4400 Long Prairie Road Flower Mound, TX 75028 
["THPHRockwall",    32.884425, -96.466031, campusradius], # Texas Health Presbyterian Hospital Rockwall 3150 Horizon Road Rockwall, TX 75032 
]

# Other locations that are similar to above locations
controlsites=[
["Maryland",  39.003409, -77.104474, caseradius], # NIH Clinical Center, National Institutes of Health, 10 Center Drive, Bethesda, MD 20814
["Georgia",   33.792749, -84.321321, caseradius], # Emory University Hospital, 1364 Clifton Road Northeast, Atlanta, GA 30322
["Kansas",    37.6907,   -97.3427,   caseradius], # Kansas, LA, San Diego, and Colorado are similar to cities exposed to Ebola
["LA",        34.0194,   -118.4108,  caseradius],
["SanDiego",  32.8153,   -117.1350,  caseradius],
["Colorado",  38.8673,   -104.7607,  caseradius],
["Boston",    42.3320,   -71.0202,   caseradius]
]

# WIDE OPEN DATES 2014-2015
wotime1=datetime(2014,1,1)
wotime2=datetime(2015,1,1)

# Survey period
sptime1=datetime(2014,10,29)
sptime2=datetime(2014,11,15)

# Thomas Duncan
tdtime1=datetime(2014,9,30)
tdtime2=datetime(2014,10,01)

# Nina Pham 
nptime1=datetime(2014,10,12)
nptime2=datetime(2014,10,13)

# Amber Vinson
avtime1=datetime(2014,10,15)
avtime2=datetime(2014,10,16)
#avtime2=datetime(2014,10,17) # Temporary change to 3 day window for testing

# Craig Spencer
cstime1=datetime(2014,10,23)
cstime2=datetime(2014,10,24)

