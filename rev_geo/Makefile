# examples for reference
somePath/someFile.txt: stuff
	echo $@
	echo $(dir $@)
	echo $(notdir $@)
	echo $<

stuff:
	echo $@
	echo $(notdir $@)

# run `make data/tl_2013_us_county.shp` 
data/tl_2013_us_county.zip:
	mkdir -p $(dir $@)
	curl -o $@ ftp://ftp2.census.gov/geo/tiger/TIGER2013/COUNTY/$(notdir $@)

data/tl_2013_us_county.shp: data/tl_2013_us_county.zip
	unzip -d $(dir $@) $<


