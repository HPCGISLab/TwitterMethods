#!/usr/bin/python
"""
Copyright (c) 2014 High-Performance Computing and GIS (HPCGIS) Laboratory. All rights reserved.
Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.
Authors and contributors: Eric Shook (eshook@kent.edu);
Website: http://hpcgis.geog.kent.edu
"""

import sys,os
import json
import codecs
import pprint
from multiprocessing import Pool
import copy

from .distance import *

pp=pprint.PrettyPrinter(indent=2)

# Print output of an object in unicode format, which solves a problem when piping the output
def uprint(toprint):
    print toprint.encode('utf-8')

# Print output of an object in unicode format, which solves a problem when piping the output
# This also wraps it up in pretty print for formatting.
# Note: this function should only be used for debugging
def upprint(toprint):
    pp.pprint(toprint)

# Error function, which removes output file in case of an error
# This is important to not mask problems and have half output files before an error.
def error(infilename,outfilename,msg):
    print(" [ ERROR ]:",msg," infilename:",infilename,"outfilename:",outfilename)
    if(os.path.isfile(outfilename)):
        print(" Deleting output file",outfilename)
        os.remove(outfilename)
    raise
    exit()

# Make sure input files exist and output directories are created
def sanitycheck(infilename,outfilename):
    if(not os.path.exists(infilename)):
        print(" [ ERROR ] Sanity check failed - Input file does not exist",infilename)
        error(infilename,outfilename,"file does not exist")
    if(not os.path.exists(os.path.dirname(outfilename))):
        os.makedirs(os.path.dirname(outfilename))
        print(" Creating output directory:",outfilename)
    if(os.path.exists(outfilename)):
        print(" Removing already existing output file:",outfilename)
        os.remove(outfilename)    

# This utility function checks whether a file is empty, and if so it removes it
# This is useful, because GNIP organizes tweets in 10 min increments so for smaller
# areas you end up with many empty files. This saves scripts from "processing"
# thousands of empty files over and over.
def checkandremoveemptyfile(filename):
   try:
       if(os.stat(filename).st_size == 0): # Check if it is empty
           os.remove(filename) # If so, then remove it
   except:  # We don't care if it errors
       pass # So pass
   return

# Helpful to get a list of files in a directory with a certain extension
def filesindir(dirname,extensionstring):
    filelist=[]
    for root, dirs, filenames in os.walk(dirname):
        for file in filenames:
            if file.endswith(extensionstring):
                filelist.append(file)
    return filelist

# List of json files in a directory
def jsonindir(dirname):
    return filesindir(dirname,".json")

# List of csv files in a directory
def csvindir(dirname):
    return filesindir(dirname,".csv")

# Helpful to get a list of files in a directory 
def dirtofilelist(dirname,filelist):
    for i in xrange(len(filelist)):
        filelist[i]=os.path.join(dirname,filelist[i])
    return filelist

# Process all the files from input directory in parallel using numprocs
# This is done by applying funct to files in the input directory
# In general output files will be saved in outdir
def process(funct,indir,outdir,numprocs):
    filelist=jsonindir(indir)
    infilelist=copy.copy(filelist)
    outfilelist=copy.copy(filelist)

    # Loop over all files in file list (json files in indir)
    # Create two lists, one for input files and one for output files (with the same name)
    for i in xrange(len(filelist)):
        infilelist[i]=os.path.join(indir,filelist[i])
        outfilelist[i]=os.path.join(outdir,filelist[i])

    combinedfilelist=zip(infilelist,outfilelist)

    # Apply funct to each input/output file using parallel pool of processes
    pool = Pool(processes=numprocs)
    pool.map(funct,combinedfilelist)
    pool.close()

