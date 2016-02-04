#!/usr/bin/python

import tweetproc 
import os
import io
from datetime import *
from tweetproc.sitesdata import * 

# Global variable used for processing
siteiter=-1

# Custom process for this script
def process(inputdir,outfilename,tictime1,tictime2):

        # Empty dictionary to store the tweet counts for each user
	userlist={}

        # Process all the files in the input directory
	filelist=tweetproc.jsonindir(inputdir)
	for file in filelist:
	    usercounts=tweetproc.mtic(os.path.join(inputdir,file),tictime1,tictime2)

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
        outfilename="csv/out.mtic-sites-"+sites[siteiter][0]+"-"+str(radius)+"-"+str(tictime1.date())+"-"+str(tictime2.date())+".csv"

        process(inputdir,outfilename,tictime1,tictime2)

# Calculate TIC for KSU campuses when Amber Vinson was diagnosed and during the survey period
runtic(tweetproc.campussites,avtime1,avtime2)
runtic(tweetproc.texassites,tdtime1,tdtime2)
runtic(tweetproc.campussites,sptime1,sptime2)
'''
'''


# Calculate TIC for US-Diagnosed Ebola case locations for each Ebola case
'''
runtic(casesites,tdtime1,tdtime2)
runtic(casesites,nptime1,nptime2)
runtic(casesites,avtime1,avtime2)
runtic(casesites,cstime1,cstime2)
'''

