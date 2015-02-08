#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Brian Lehman, Scott Hendrickson"


import sys
import re
import codecs

reload(sys)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)

import math
import pprint
import json
import fiona
from shapely.geometry import Point, shape, Polygon, box 
from collections import defaultdict
import argparse
import os
import pickle 

########################
# functions 

def tree(): return defaultdict(tree)

def grid_finder(x,y):
    return (int((math.floor(x)-grid_boundaries[0])/delta)
           ,int((math.floor(y)-grid_boundaries[1])/delta))

def topic_args():
    parser = argparse.ArgumentParser(description="Reverse geo coder returns location info given a set of lon,lat")
    parser.add_argument("file_name"
            , metavar= "file_name"
            , nargs="?"
            , default=[] 
            , help="Input file name (optional).")
    parser.add_argument("-b"
            , "--bounding-box"
            , dest="grid_boundaries"
            , default="-185,15,-65,70"
            , help="Set bounding box for region to include (default: [-185,15,-65,70])")
    parser.add_argument("-d"
            , "--delta"
            , dest="delta"
            , default=5
            , help="Set the number of degrees between grid coords (default: 5)")
    parser.add_argument("-g"
            , "--use-saved-grid"
            , dest="use_saved_grid"
            , default=False
            , action="store_true"
            , help="Save grid or use previously saved version in data/grid.json")
    parser.add_argument("-s"
            , "--shape-file-path"
            , dest="shape_file_path"
            , default="data/tl_2013_us_county.shp"
            , help="Set shapefile path (default: data/tl_2013_us_county.shp)")
    parser.add_argument("-t"
            , "--tweet-input"
            , dest="tweet_input"
            , default=False
            , action="store_true"
            , help="Set input as tweet payload instead of coordinates (in progress)")
    return parser

def build_grid():
    #grid_boundaries=(-185,15,-65,70) # upright edge is plus delta (lower 48 states)
    grid={(i,j):{}
            for i in range((grid_boundaries[2]-grid_boundaries[0])/delta) 
            for j in range((grid_boundaries[3]-grid_boundaries[1])/delta) }
 
    with fiona.open(options.shape_file_path) as fc: 
        print >>sys.stderr, fc.driver,"###",fc.schema,"###", len(fc),"###",fc.crs
        print >> sys.stderr,fc.schema
        print >>sys.stderr, "Number of records:", len(fc)
        print >>sys.stderr, "Bounds of all records:", fc.bounds
        print >>sys.stderr, "Bounds applied:",grid_boundaries
        print >> sys.stderr,"######## indexing shapes to grid ########"
        print >> sys.stderr,"shapes complete:"
        c=0
        for feature in fc: 
            c+=1
            GEOID=str(feature['properties']['GEOID'])
            NAME=feature['properties']['NAME']
            INTPTLON=float(feature['properties']['INTPTLON'])
            INTPTLAT=float(feature['properties']['INTPTLAT'])
            shp=shape(feature['geometry']) # list of coordinates of geometric shape
            bb=box(*shp.bounds) #box(minx,miny,maxx,maxy)) creates one boxlike shape to rule them all
            for i,j in grid:
                grid_box=box(i*delta+grid_boundaries[0]
                            ,j*delta+grid_boundaries[1]
                            ,(i+1)*delta+grid_boundaries[0]
                            ,(j+1)*delta+grid_boundaries[1] )
                if grid_box.intersects(bb): #http://toblerity.org/shapely/manual.html#object.intersects
                    grid[(i,j)][bb]=(shp,GEOID,NAME,INTPTLON,INTPTLAT) # (county shape, countyID)
            if c%100==0:
                print >> sys.stderr, c
    return grid
    

if __name__ == '__main__':
    options = topic_args().parse_args()
    grid_boundaries=[int(item) for item in options.grid_boundaries.split(",")]
    delta=int(options.delta)
    if not options.use_saved_grid:
        grid=build_grid()
    else:
        if not os.path.isfile("./data/grid.json"):
            print >>sys.stderr, "creating ./data/grid.json"
            grid=build_grid()
            if not os.path.exists("./data"):
                os.makedirs("./data")
            print >>sys.stderr, "saving file ./data/grid.json"
            with open("./data/grid.json","wb") as g:
                pickle.dump(grid,g)
        else:
            print >>sys.stderr, "using ./data/grid.json"
            grid=pickle.load(open("./data/grid.json"))
    counter=0
    in_grid_not_in_county=0
    grid_counter=0
    print >> sys.stderr,"######## locating geo coords in grid ########"
    for line in sys.stdin:
        #( lng, lat ) = coord #NOTE:the input file must contain (lng,lat)
        values=line.replace("(","").replace(")","").replace("[","").replace("]","").strip().split(",")
        lng = float(values[0])
        lat = float(values[1])
        point = Point(float(lng), float(lat))
        coords=grid_finder(lng,lat)
        found=False
        if coords not in grid:
            counter+=1
            print >> sys.stderr,"not in grid:{},not in county:{},found{}".format(counter,in_grid_not_in_county,grid_counter)
            print >> sys.stderr,"{},{}: not in grid".format(lng,lat)
            continue
        for box in grid[coords]:
            if box.contains(point):
                if grid[coords][box][0].contains(point):
                    e=tree()
                    found=True
                    grid_counter+=1
                    e["coords"]=(lng,lat)
                    e["GEOID"]=grid[coords][box][1]
                    e["centroid"]=(grid[coords][box][3],grid[coords][box][4])
                    e["county"]=grid[coords][box][2]
                    print json.dumps(e)
                    break #point found, no need to continue searching
        if not found:
            in_grid_not_in_county+=1
    print >> sys.stderr,"######## DONE  ########"
    print >> sys.stderr, "{} points outside of grid".format(counter) 
    print >> sys.stderr, "{} points in grid but not in a county".format(in_grid_not_in_county) 
    print >> sys.stderr, "{} points in grid and in county".format(grid_counter) 

