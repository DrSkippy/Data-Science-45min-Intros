# Makefile
Creating a *`Makefile`* allows others to recreate necessary components of your work flow while managing unecessary steps.

###Why do this now?
The *`Makefile`* process can be useful when working with shapefiles. Instead of carrying large .shp files around in a repo, we'll give anyone the opportunity to create the files.  

###Makefile terminology and symbols
Pseudo code for each section of a *`Makefile`* is as follows.  

`Target: dependency`  
&nbsp; `commands to run`

The following variables come in handy when writing make files.  
&nbsp; `$@` =  `target`   
&nbsp; `$(dir $@)` = `target directory`  
&nbsp; `$(notdir $@)` = `target filename`  
&nbsp; `$<` = `dependency`   

###Example
For example, we could create a target named `somePath/someFile.txt` that depends on first building `stuff`.  

`stuff`:  
&nbsp; `echo $@`  
&nbsp; `echo $(notdir $@)`  

`somePath/someFile.txt: stuff`  
&nbsp; `echo $@`  
&nbsp; `echo $(dir $@)`  
&nbsp; `echo $(notdir $@)`  
&nbsp; `echo $<`  
 
 To see this example execute, run the following script from the command line within the gis_tools directory. 
 <pre> make somePath/someFile.txt </pre> 

# Shapefiles

The [terminology](https://www.census.gov/geo/maps-data/data/pdfs/tiger/tgrshp2013/TGRSHP2013_TechDoc_Ch4.pdf) for shapefiles can be a little confusing, but the main ideas will be discussed below.

First, let's get some data. To download a zip file containing county data and then upzip it in a new `data` directory, please run the following script from the command line within the gis_tools directory.  
<pre> make data/tl_2013_us_county.shp </pre>  
When it finishes, you can view the files in the `gis_tools/data` directory. These files were downloaded from the US Census Bureau. 

* [Click](https://www.census.gov/geo/maps-data/data/tiger.html) for more information about the census data used in this example.   

### What's inside a shapefile? 
We'll use python's `fiona` and `shapely` packages to view the contents of the shapefile and determine geometric properties of the corresponding features. 

<pre>
#!/usr/bin/env python
import pprint
import fiona


with fiona.open("data/tl_2013_us_county.shp") as fc: 
    print "File type:",fc.driver
    print "Schema:",pprint.pprint(fc.schema)
    print "Number of records:", len(fc)
    print "Bounds of all records:", fc.bounds #visit http://boundingbox.klokantech.com/ to view these coords
    print "Additional info (coordinate reference system):", fc.crs
    print "Field type map:"
    pprint.pprint(fiona.FIELD_TYPES_MAP)
    records=list(fc)
</pre>

###Features
* The collection (fc) contains 3,234 records or features. 
* Each feature is a Python dict structured exactly like a [GeoJSON](http://geojson.org/) Feature. 
* Each feature starts and ends with the same point (eg. complete polygon)
* Each feature (in this example) contains information about a specific county.
* [Click](http://toblerity.org/fiona/manual.html) for more information about `fiona`.   
* [Click](http://www.census.gov/geo/reference/ansi.html) for codes related to the features' 'properites'.  
* [Click](https://www.census.gov/geo/maps-data/data/pdfs/tiger/tgrshp2013/TGRSHP2013_TechDoc_A.pdf) for codes specific to county features (page A-80).

<pre>
#!/usr/bin/env python
import fiona
import pprint


pprint.pprint(records[0])
print 
print
print "###########################"
print "alternative method below"
print "###########################"
print 
print 
with fiona.open("data/tl_2013_us_county.shp") as fc: 
    first=True
    for record in fc:
        if first:
            print pprint.pprint(record)
            break
</pre>

###Analyzing features
* use Python's 'shapely' package.
* [Click](http://toblerity.org/shapely/manual.html#object.intersects) for documentation on evaluating if shapes intersect. 
* [Click](http://toblerity.org/shapely/manual.html#object.contains) for documentation on evaluating if points are contained within shapes.

<pre>
import fiona
from shapely.geometry import Point, shape, Polygon, box

#print records[0]
#print shape(records[0]["geometry"]) # one feature converted to shapley polygon object

print "{} Shapley object: {}".format(records[0]['properties']['NAMELSAD'],box(*shape(records[0]["geometry"]).bounds))
print
shp1 = box(*shape(records[0]["geometry"]).bounds)
print "{} Shapley object: {}".format(records[1]['properties']['NAMELSAD'],box(*shape(records[1]["geometry"]).bounds))
print 
shp2 = box(*shape(records[1]["geometry"]).bounds)
print "Does {} intersect {}?".format(records[0]['properties']['NAMELSAD'],records[1]['properties']['NAMELSAD'])
print "{}".format(shp1.intersects(shp2)) 
print 
print "Is (-123.4688,46.2674) in {}?".format(records[0]['properties']['NAMELSAD'])
p1=Point(-123.4688,46.2674)
print "{}".format(shape(records[0]["geometry"]).contains(p1))
print
print "Is (-123.4688,46.2674) in {}?".format(records[1]['properties']['NAMELSAD'])
print "{}".format(shape(records[1]["geometry"]).contains(p1))
print 
print "Create a list of centroids for every county."
centroids=[]
with fiona.open("data/tl_2013_us_county.shp") as fc: 
    with open("data/centroids.txt","wb") as cntr:
        for feature in fc:
            pt=(float(feature["properties"]["INTPTLON"]),float(feature["properties"]["INTPTLAT"]))
            centroids.append(pt)
            cntr.write(str(pt)+'\n')
print "{} centroids created".format(len(centroids))
</pre>
###Utilities
Two tools that can be handy when working with shapefiles:
* ogr2ogr - part of [GDAL](http://www.gdal.org/) that merges multiple .shp files into a single [GeoJson](http://geojson.org/) file (among many other features).
* [topojson](https://github.com/mbostock/topojson/wiki) - shrinks GeoJson files to a convenient format. 

[Example](http://bost.ocks.org/mike/map) that uses both tools.

#Using rev_geo.py
This utility takes coordinates and returns location information, but requires the user to point at the tl_2013_us_county.shp file. 
* currently only available for US state/county info

###Standard options
The options are rather limited at this point.
* points outside of the US are currently excluded.  
* considerations:   
&nbsp; 1.  general solution for an efficiency grid indpendent of shapefile used.

<pre>
usage: rev_geo.py [-h] [-b GRID_BOUNDARIES] [-d DELTA] [-g]
                  [-s SHAPE_FILE_PATH] [-t]
                  [file_name]

Reverse geo coder returns location info given a set of lon,lat

positional arguments:
  file_name             Input file name (optional).

optional arguments:
  -h, --help            show this help message and exit
  -b GRID_BOUNDARIES, --bounding-box GRID_BOUNDARIES
                        Set bounding box for region to include (default:
                        [-185,15,-65,70])
  -d DELTA, --delta DELTA
                        Set the number of degrees between grid coords
                        (default: 5)
  -g, --use-saved-grid  Save grid or use previously saved version in
                        data/grid.json
  -s SHAPE_FILE_PATH, --shape-file-path SHAPE_FILE_PATH
                        Set shapefile path (default:
                        data/tl_2013_us_county.shp)
  -t, --tweet-input     Set input as tweet payload instead of coordinates (in
                        progress)
</pre>
###Standard output
The general form of the output includes the following:
* county: str [county name]  
* centroid: (longitude, latitude)  [center of county]  
* coords: (longitude, latitude) [specific coords passed to rev_geo.py]  
* GEOID: int(5) [state_code + county_code]  
<pre>
{"county": "Wahkiakum", 
 "centroid": [-123.4244583, 46.2946377], 
 "coords": [-123.4244583, 46.2946377], 
 "GEOID": "53069"}
</pre>

###Example script
<pre>
$head data/centroids.txt | ./rev_geo.py -g > info.json
$cat info.json
{"county": "Cuming", "centroid": [-96.7885168, 41.9158651], "coords": [-96.7885168, 41.9158651], "GEOID": "31039"}
{"county": "Wahkiakum", "centroid": [-123.4244583, 46.2946377], "coords": [-123.4244583, 46.2946377], "GEOID": "53069"}
{"county": "De Baca", "centroid": [-104.3686961, 34.3592729], "coords": [-104.3686961, 34.3592729], "GEOID": "35011"}
{"county": "Lancaster", "centroid": [-96.6886584, 40.7835474], "coords": [-96.6886584, 40.7835474], "GEOID": "31109"}
{"county": "Nuckolls", "centroid": [-98.0468422, 40.1764918], "coords": [-98.0468422, 40.1764918], "GEOID": "31129"}
{"county": "Las Piedras", "centroid": [-65.871189, 18.1871483], "coords": [-65.871189, 18.1871483], "GEOID": "72085"}
{"county": "Minnehaha", "centroid": [-96.7957261, 43.6674723], "coords": [-96.7957261, 43.6674723], "GEOID": "46099"}
{"county": "Menard", "centroid": [-99.8539896, 30.8843655], "coords": [-99.8539896, 30.8843655], "GEOID": "48327"}
{"county": "Sierra", "centroid": [-120.5219926, 39.5769252], "coords": [-120.5219926, 39.5769252], "GEOID": "06091"}
{"county": "Clinton", "centroid": [-85.1534262, 36.7288647], "coords": [-85.1534262, 36.7288647], "GEOID": "21053"}
</pre>




