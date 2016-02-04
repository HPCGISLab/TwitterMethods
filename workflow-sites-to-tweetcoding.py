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
def process(inputdir,outfilename,tctime1,tctime2):

        # Empty dictionary to store the tweet counts for each user
	userlist={}

        # Process all the files in the input directory
	filelist=tweetproc.jsonindir(inputdir)
	for file in filelist:
            # Returns a dictionary of user ids with the counts of each behavior response for that user
	    usertccounts=tweetproc.tweetcoding(os.path.join(inputdir,file),tctime1,tctime2)

            print usertccounts

            # Loop over all of the users in the usertcs dictionary returned by the tcesponse method
            # If the user is already in userlist, then add the behavior response counts, otherwise set the counts
	    for user in usertccounts:
		if user in userlist: # If user is already in the user list
                    for tc in usertccounts[user]: # Loop over all the behavior responses
		        userlist[user][tc]+=usertccounts[user][tc] # Add each to the existing count
		else:
		    userlist[user]=usertccounts[user] # Just copy the behavior count dictionary over
        print "Processing",outfilename

        #pprint.pprint(userlist)

        # Save the results
	with io.open(outfilename,'w',encoding="utf-8",errors='ignore') as outfile:
            # Loop over all users in the userlist and save the values to the CSV file
	    for user, tccounts in sorted(userlist.items()):
		userstr=user
                for tc in tccounts:
		    userstr=userstr+","+str(tccounts[tc])
                userstr+="\n"
		outfile.write(unicode(userstr))

	        tcsummary={'concern':0,
                 'experience':0,
                 'opinion':0,
                 'sarcasm':0,
                 'relief':0,
                 'downplay':0,
                 'frustration':0,
                 'total':0
                }

            # Loop over all users in the userlist and summarize the number of behavior responses 
	    for user, tccounts in sorted(userlist.items()):
                for tc in tccounts:
                    print "user",user,"tc",tc,"tccounts[tc]",tccounts[tc],"tcsum[tc]",tcsummary[tc]
                    tcsummary[tc]+=tccounts[tc]
            sum=len(userlist)

            # For convenience calculate the ratio of users for each category 
            # Write out the percentage of users with the count 
	    for tc in tcsummary: 
                if sum>0:
                    percent=float(tcsummary[tc]*100)/float(sum)
                else:
                    percent=0.0
		outfile.write(unicode(str(tc)+","+str(tcsummary[tc])+","+str(round(percent,2))+"\n"))
            # Then write out the sum
	    outfile.write(unicode("sum,"+str(sum)+"\n"))

# Run tweet coding for multiple sites (lists defined above) 
def runtccoding(sites,tctime1,tctime2):

    global siteiter

    # Loop over each site in the sites list
    for i in xrange(len(sites)):
        siteiter=i
        print "Processing",sites[siteiter][0]
        radius=sites[siteiter][3]

        # Calculate which input directory to process based on the site information (name and radius)
        inputdir="data/geoebola-sites-"+sites[siteiter][0]+"-"+str(radius)

        # Generate a CSV output file to save tweet coding results
        outfilename="csv/out.tweetcoding-sites-"+sites[siteiter][0]+"-"+str(radius)+"-"+str(tctime1.date())+"-"+str(tctime2.date())+".csv"

        process(inputdir,outfilename,tctime1,tctime2)


# Calculate Behavior Response for KSU campuses when Amber Vinson was diagnosed and during the survey period
#runtccoding(campussites,avtime1,avtime2)
runtccoding(campussites,sptime1,sptime2)

