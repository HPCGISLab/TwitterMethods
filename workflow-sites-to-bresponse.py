#!/usr/bin/python

import tweetproc 
import os
import io
from datetime import *
from tweetproc.sitesdata import * 
import pprint

# Global variable used for processing
siteiter=-1

# Custom process for this script
def process(inputdir,outfilename,brtime1,brtime2):

        # Empty dictionary to store the tweet counts for each user
	userlist={}

        # Process all the files in the input directory
	filelist=tweetproc.jsonindir(inputdir)
	for file in filelist:
            # Returns a dictionary of user ids with the counts of each behavior response for that user
	    userbrcounts=tweetproc.tweetcodingbresponse(os.path.join(inputdir,file),brtime1,brtime2)

            # Loop over all of the users in the userbrs dictionary returned by the bresponse method
            # If the user is already in userlist, then add the behavior response counts, otherwise set the counts
	    for user in userbrcounts:
		if user in userlist: # If user is already in the user list
                    for br in userbrcounts[user]: # Loop over all the behavior responses
		        userlist[user][br]+=userbrcounts[user][br] # Add each to the existing count
		else:
		    userlist[user]=userbrcounts[user] # Just copy the behavior count dictionary over
        print "Processing",outfilename

        #pprint.pprint(userlist)

        # Save the results
	with io.open(outfilename,'w',encoding="utf-8",errors='ignore') as outfile:
            # Loop over all users in the userlist and save the values to the CSV file
	    for user, brcounts in sorted(userlist.items()):
		userstr=user
                for br in brcounts:
		    userstr=userstr+","+str(brcounts[br])
                userstr+="\n"
		outfile.write(unicode(userstr))

	    brsummary={'handwash':0,
                 'handsanitize':0,
                 'cough':0,
                 'avoidgathering':0,
                 'avoidschool':0,
                 'total':0
            }

            # Loop over all users in the userlist and summarize the number of behavior responses 
	    for user, brcounts in sorted(userlist.items()):
                for br in brcounts:
                    print "user",user,"br",br,"brcounts[br]",brcounts[br],"brsum[br]",brsummary[br]
                    brsummary[br]+=brcounts[br]
            sum=len(userlist)

            # For convenience calculate the ratio of users for each category 
            # Write out the percentage of users with the count 
	    for br in brsummary: 
                if sum>0:
                    percent=float(brsummary[br]*100)/float(sum)
                else:
                    percent=0.0
		outfile.write(unicode(str(br)+","+str(brsummary[br])+","+str(round(percent,2))+"\n"))
            # Then write out the sum
	    outfile.write(unicode("sum,"+str(sum)+"\n"))

# Run behavior response coding for multiple sites (lists defined above) 
def runbrcoding(sites,brtime1,brtime2):
    global siteiter
    # Loop over each site in the sites list
    for i in xrange(len(sites)):
        siteiter=i
        print "Processing",sites[siteiter][0]
        radius=sites[siteiter][3]

        # Calculate which input directory to process based on the site information (name and radius)
        inputdir="data/geoebola-sites-"+sites[siteiter][0]+"-"+str(radius)

        # Generate a CSV output file to save behavior response results
        outfilename="csv/out.br-sites-"+sites[siteiter][0]+"-"+str(radius)+"-"+str(brtime1.date())+"-"+str(brtime2.date())+".csv"

        process(inputdir,outfilename,brtime1,brtime2)


# Calculate Behavior Response for KSU campuses when Amber Vinson was diagnosed and during the survey period
#runbrcoding(campussites,avtime1,avtime2)
runbrcoding(campussites,sptime1,sptime2)

