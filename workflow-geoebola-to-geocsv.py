#!/usr/bin/python

import tweetproc 
import os
import io

inputdir="data/geoebola-sites-Kent-25000"
inputdir="data/geoebola"

outfilename="csv/out.geoebola.csv"

# Start with an empty string
outputstring=""

filelist=tweetproc.jsonindir(inputdir)
for file in filelist:
    outputstring=outputstring+tweetproc.geocsv(os.path.join(inputdir,file))

with io.open(outfilename,'w',encoding="utf-8",errors='ignore') as outfile:
    outfile.write(outputstring)

