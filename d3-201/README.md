# D3-201
This lecture focuses on illustrating [Bostock's reusable charts](http://bost.ocks.org/mike/chart/)
technique with a simple example for efficiently building multiple instances of the
same chart.  

### Why D3?
For presentation ready charts that are fully customizable and interactive on
a web based display (or as a static image if necessary).  

In the past, ggplot (from the R library) served most needs for our team. As
our client presentations grew in scope or as the marketing team
recognized new opportunities, so did the need for
customization. The D3 javascript library exposes data visualization at a
level that template oriented design falls short.  

### Why reusable?
Template based graphs, like ggplot for R, can be handy! They are generally quick to use and provide a baseline of customize that can potentially satisfy a wide range of use cases, but at some point, the customization options can be limited.  

This example builds something close to a javascript charting template that comes with all of the limitations of a regular template options. This might be useful in the following cases:
1. We wrote a superb graph that we want to replicate using several data
   sources.
2. We want to quickly alter a graph that we've previously built.
3. We want others to be able to easily reuse our chart.

### Tutorial

##### Part I: Render 
The first step is to set up our directory structure. Run the following
command:
<pre>
$ cd D3-201
$ ./_setup_dirs_.py
</pre>
We should see the following new files.  
<br>
<img src="img/file.png" alt="Drawing" style="width: 600px;"/>  
</br>
This set up allows us to render the index.html that then sources files
from the other folders. Open up the index.html file and look at the
structure. Explore and try to determine where these sources point and
take a guess:  

1. [basic] What is the purpose of each sourced file?  
2. [intermediate] What determines the number of graphs we will
   create?  
3. [advanced] How does the graph access the data?  

Let's experiment with the code and see if we can answer some of the
abpve questions. We will start by exploring the graph and rendering the
file.
<pre>
$ cd D3-201
$ python -m SimpleHTTPServer 8080
</pre>
Point your Chrome browser to [localhost:8080](http://localhost:8080/).
We should see two heatmaps.  

##### Part II: Explanation of app.js
Open `js/app.js` a text editor.  
1. [basic] Where is `heatmap` invoked?  
2. [basic] What do you think happens when we use `myHeatmap.height()`?  
3. [intermediate] Why are we iterating over dataPathArray on line 12?  
4. [advanced] What is the value of `myHeatmap`?  

##### Part III: Explanation of heatmap.js
Open `js/heatmap.js` in text editor.  
1. [basic] Why do we love python? (see lines 3-49)  
2. [basic] How can I change the color of both charts?  
3. [intermediate] How can I change the color of just one chart?  
4. [advanced] When is the function `chart` invoked?  
5. [advanced] What does `myHeatmap()` expect and why?  



