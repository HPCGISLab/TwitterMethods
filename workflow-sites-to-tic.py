#!/usr/bin/python

import tweetproc 
import os
import io
from datetime import *
from tweetproc.sitesdata import * 

'''
caseradius=100000
caseradius=50000
campusradius=15000
campusradius=25000

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

texassites=[
["THPHDallas",      32.881525, -96.762410, campusradius], # Texas Health Presbyterian Hospital Dallas, 8200 Walnut Hill Lane, Dallas, TX 75231 (duplicate)
["THPHAllen",       33.116341, -96.673193, campusradius], # Texas Health Presbyterian Hospital Allen 1105 Central Expressway Allen, TX 75013 
["THPHDenton",      33.217850, -97.166504, campusradius], # Texas Health Presbyterian Hospital Denton 3000 North I-35 Denton, TX 76201 
["THPHKaufman",     32.591426, -96.318062, campusradius], # Texas Health Presbyterian Hospital Kaufman 850 Ed Hall Drive Kaufman, TX 75142 
["THPHPlano",       33.044414, -96.835895, campusradius], # Texas Health Presbyterian Hospital Plano 6200 West Parker Road Plano, TX 75093 
["THPHFlowerMound", 33.045827, -97.067547, campusradius], # Texas Health Presbyterian Hospital Flower Mound 4400 Long Prairie Road Flower Mound, TX 75028 
["THPHRockwall",    32.884425, -96.466031, campusradius], # Texas Health Presbyterian Hospital Rockwall 3150 Horizon Road Rockwall, TX 75032 
]


casesites=[
#Sitename    #Latitude  #Longitude  #Radius (meters)
["Ohio",      41.071312, -81.400874, caseradius], # Stonegate Trail, Tallmadge, OH (Development where Amber Vinson stayed while in Ohio)
["Texas",     32.881525, -96.762410, caseradius], # Texas Health Presbyterian Hospital Dallas, 8200 Walnut Hill Lane, Dallas, TX 75231
["NewYork",   40.738766, -73.975368, caseradius]  # Bellevue Hospital Center, 462 1st Avenue, New York, NY 10016
]

controlsites=[
["Maryland",  39.003409, -77.104474, caseradius], # NIH Clinical Center, National Institutes of Health, 10 Center Drive, Bethesda, MD 20814
["Georgia",   33.792749, -84.321321, caseradius], # Emory University Hospital, 1364 Clifton Road Northeast, Atlanta, GA 30322
["Kansas",    37.6907,   -97.3427,   caseradius],
["LA",        34.0194,   -118.4108,  caseradius],
["SanDiego",  32.8153,   -117.1350,  caseradius],
["Colorado",  38.8673,   -104.7607,  caseradius],
["Boston",    42.3320,   -71.0202,   caseradius]
]

# WIDE OPEN DATES 2014-2015
wotime1=datetime(2014,1,1)
wotime2=datetime(2015,1,1)

# Survey period
sptime1=datetime(2014,10,28)
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

# Craig Spencer
cstime1=datetime(2014,10,23)
cstime2=datetime(2014,10,24)
'''

# Global variable used for processing
siteiter=-1

# Custom process for this script
def process(inputdir,outfilename,tictime1,tictime2):

        # Empty dictionary to store the tweet counts for each user
	userlist={}

        # Process all the files in the input directory
	filelist=tweetproc.jsonindir(inputdir)
	for file in filelist:
	    usercounts=tweetproc.tic(os.path.join(inputdir,file),tictime1,tictime2)

            # Loop over all of the users in the usercounts dictionary returned by the tic method
            # If the user is already in userlist, then add the count, otherwise set the count
	    for user in usercounts:
		if user in userlist:
		    userlist[user]+=usercounts[user]
		else:
		    userlist[user]=usercounts[user]

        print "Processing",outfilename

	with io.open(outfilename,'w',encoding="utf-8",errors='ignore') as outfile:
            # Loop over all users in the userlist and save the values to the CSV file
	    for user, value in sorted(userlist.items()):
		userstr=user+","+str(value)+"\n"
		outfile.write(unicode(userstr))

            # Loop over all users in the userlist and classify the user based on the number of tweets
            # The count goes from 1-5.
	    counts=[0,0,0,0,0,0]
	    for user, value in sorted(userlist.items()):
		if value >= 5:
		    counts[5]+=1
		else:
		    counts[value]+=1
            sum=len(userlist)

            # For convenience calculate the ratio of users in each category
            # Write out the percentage of users with 1, 2, 3, 4, 5+ tweets
	    for i in xrange(0,len(counts)):
                if sum>0:
                    percent=float(counts[i]*100)/float(sum)
                else:
                    percent=0.0
		outfile.write(unicode(str(i)+","+str(counts[i])+","+str(round(percent,2))+"\n"))
            # Then write out the sum
	    outfile.write(unicode("sum,"+str(sum)+"\n"))

# Run TIC for multiple sites (lists defined above) 
def runtic(sites,tictime1,tictime2):

    # Loop over each site in the sites list
    for i in xrange(len(sites)):
        siteiter=i
        radius=sites[siteiter][3]
        print "Processing",sites[siteiter][0],"radius",radius

        # Calculate which input directory to process based on the site information (name and radius)
        inputdir="data/geoebola-sites-"+sites[siteiter][0]+"-"+str(radius)

        # Generate a CSV output file to save TIC results
        outfilename="csv/out.tic-sites-"+sites[siteiter][0]+"-"+str(radius)+"-"+str(tictime1.date())+"-"+str(tictime2.date())+".csv"

        process(inputdir,outfilename,tictime1,tictime2)

# Calculate TIC for KSU campuses when Amber Vinson was diagnosed and during the survey period
runtic(tweetproc.campussites,avtime1,avtime2)
'''
runtic(tweetproc.campussites,sptime1,sptime2)
'''


'''
# Calculate TIC for US-Diagnosed Ebola case locations for each Ebola case
#runtic(casesites,tdtime1,tdtime2)
#runtic(casesites,nptime1,nptime2)
#runtic(casesites,avtime1,avtime2)
#runtic(casesites,cstime1,cstime2)
'''

#runtic(campussites,tdtime1,tdtime2)
#runtic(texassites,tdtime1,tdtime2)
#runtic(texassites,nptime1,nptime2)
#runtic(texassites,avtime1,avtime2)
#runtic(texassites,cstime1,cstime2)

