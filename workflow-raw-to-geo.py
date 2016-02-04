#!/usr/bin/python

import tweetproc 
import os
from multiprocessing import Pool
import copy

# Apply geo function to each file extracting geo-enabled tweets 
def runit(params):
    tweetproc.geo(*params)

'''
# FIXME: This has been moved to util.py
# Process the files in parallel
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

# Process 'raw' directory and save all geo-enabled tweets in 'geo' directory
inputdir="data/raw"
outputdir="data/geo"

# Process the files using 12 cores
tweetproc.process(runit,inputdir,outputdir,12)


