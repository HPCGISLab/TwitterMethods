#!/usr/bin/python

import tweetproc 
import os
from multiprocessing import Pool
import copy

# Apply keyword function to each file with a keyword of 'ebola'
def runit(params):
    plist=list(params)
    plist.append("ebola")
    tweetproc.keyword(*plist)

'''
# FIXME: This has been moved to util.py
# Process all the files from input directory in parallel
def process(funct,indir,outdir,numprocs):
    filelist=tweetproc.jsonindir(indir)
    infilelist=copy.copy(filelist)
    outfilelist=copy.copy(filelist)

    for i in xrange(len(filelist)):
        infilelist[i]=os.path.join(indir,filelist[i])
        outfilelist[i]=os.path.join(outdir,filelist[i])

    combinedfilelist=zip(infilelist,outfilelist)
   
    pool = Pool(processes=numprocs)
    pool.map(funct,combinedfilelist)
    pool.close()
'''    

inputdir="data/geo"
outputdir="data/geoebola"

tweetproc.process(runit,inputdir,outputdir,12)

