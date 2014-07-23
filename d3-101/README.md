#D3 101
---------
---------
[cheat sheet](https://github.com/alignedleft/strata-d3-tutorial/blob/master/d3%20Cheat%20Sheet.pdf)

## Javascript intro
Let's start by opening a blank template. Follow these instructions in [Chrome](https://www.google.com/intl/en/chrome/browser/#brand=CHMB&utm_campaign=en&utm_source=en-ha-na-us-sk&utm_medium=ha) browser. 

*  From the `d3-101` folder, run `python -m SimpleHTTPServer 8080` 
*  Navigate to `localhost:8080/hello-d3.html` in Chrome.
*  Press `option+command+j`. 


Inside the developer window we can select `Elements` tab to view the structure of the [dom](http://en.wikipedia.org/wiki/Document_Object_Model). The `body` element contains some script (`<script> </script>`) and a paragraph (`<p> </p>`). The script that allows us to access the d3 library is highlighted below.  
![](https://github.com/blehman/Data-Science-45min-Intros/blob/master/d3-101/imgs/elements.png?raw=true)

Notice that below the `Network` tab, we can select a `Console` subtab. There's also a parent  `Console` tab. Either works for typing commands. We can now type javascript and d3 commands directly in the console.  
![](https://github.com/blehman/Data-Science-45min-Intros/blob/master/d3-101/imgs/subtab.png?raw=true)

### Array
The javascript `array` is like a python `list`.

####assignment
<pre>
my_array=['bob',5];

console.log(my_array);

my_array[2]="WEE"

console.log(my_array);

my_array.pop() <removes the last element>

console.log(my_array);

my_array.push("lucy") <adds element to last>

console.log(my_array);

my_array.splice(0,2) <removes 2 elements starting at 0>

console.log(my_array);

</pre>

####iterate
`my_array.forEach(function(d,i){ console.log(d)})`  
`for (var i = 0; i < my_array.length; i++) {`  
    `alert(my_array[i]);`  
`}`  

### Object
The javascript `object` is like a python `dict`.

####assignment
<pre>
obj = {"name":"bob","age":5};
</pre>
####special functions
<pre>
keys(obj)
values(obj)
</pre>
####assignment
<pre>
obj.gender='male'
obj['income']="$2"

delete obj['income'] 
delete obj.gender
</pre>
####iterate

`obj_keys=keys(obj)`  
`for (var i = 0; i < obj_keys.length; i++) {`  
    `alert(obj_keys[i]);`  
`}`  
### Scope 
The use of `var` sets the scope of the variable to the current context. Without `var`, the variable is global. 
<pre>
var a = 5; //global scope is forced without the use of var

function return_global_a() {
    return a;
}
function return_global_b() {
    return b;
}

function test1() {
    console.log("a in function scope:",a);
    console.log("a in global scope:",return_global_a());
};

function test2() {
    var a=2;
    console.log("a in function scope:",a);
    console.log("a in global scope:",return_global_a());
};

function test3() {
    a=3
    console.log("a in function scope:",a);
    console.log("a in global scope:",return_global_a());
};

function test4() {
    var a=7
    console.log("a in function scope:",a);
    console.log("a in global scope:",return_global_a());
};
function test5() {
    b=2
    console.log("b in function scope:",b);
    console.log("b in global scope:",return_global_b());
};
function test6() {
    console.log("b in function scope:",b);
    console.log("b in global scope:",return_global_b());
};
</pre>

##D3
### Selections
What happens when you type the following?  

`d3.append('p')` 

The `type error` is caused by the fact that we have not yet selected anything to which we can append a paragraph. Try selecting the `body` directly in the `Console`:   

`d3.select('body')`

When we hit enter, notice that the selection is an `array`. ***Selections are arrays***.  
![](https://github.com/blehman/Data-Science-45min-Intros/blob/master/d3-101/imgs/selection_array.png?raw=true)

Let's create a paragraph with some text in it. 

*  Select the `Elements` tab. 
*  Below the `Elements` tab, select the subtab labeled `Console`
*  Type `d3.select('body').append('p').text("Look, I made a paragraph!")`

Notice the dom struction immediately update!

### Types of selections:

The various was that elements are categorized creates many opportunities to make d3 selections. 


|   d3.select   |        dom         |  
| :-------------: | :----------------:   |  
| \#foo         | `<any id="foo">`   |     
| foo           | `<foo>`            |  
| .foo          | `<any class="foo">`|     
| [foo=bar]     | `<any foo="bar">`  |     
| foo bar       | `<foo><bar></foo>` |    
| foo.bar       | `<foo class="bar">`|   
| foo\#bar      | `<foo id="bar">`   |  

With these selection options, we can create new elements, assign class, and edit attributes. Notice how chaining can simplify code. 

<pre>
d3.select('body').append('div').append('p').attr('class',"BEST_P_EVER")
d3.select(".BEST_P_EVER").text('Hello world.')
d3.select(".BEST_P_EVER").style('color','blue') <'style overides css style'>
</pre>

### Chaining
Variables can be created to avoid chains of reapeated code.

<pre>
d3.select('body').append('svg')
var svg = d3.select('body svg')
</pre>

We can then continue chains from these variables.

<pre>
svg.attr('height',500)
</pre>

## Data
The 3 D’s in D3 stand for:    
    Data    
    Driven    
    Documents    
and the most important methods in D3 are those that help you map data to svg elements in your visualization.
Data in D3 is pretty much always an iterable--a list of datums that you can iterate over to generate elements, like bars in a bar chart.

Since we’re interested in visualizing social data, let’s look at a social data example:    

`d3.json("tweet_example/test_twitter_data_for_D3.json", function(data){tweet_data = data})`
For the record, everything in that anonymous function that we defined inside of the d3.json() call will execute when we load our data, although it is not necessary to put the functions we want to execute there. 

Cool. We just loaded the data file, which is simply a JSON-formatted list of JSON formatted tweet-payloads. Look at that list now.

`tweet_data`

JS reads in the JSON formatted list as a list, and each JSON formatted payload as an object. Click the arrow next to an object to inspect it further. That structure should look pretty familiar.

We’ve already appended paragraphs to an svg element, let’s append data-driven paragraphs to our document.  

define a function like this:  
<pre>  
function displayhandles(){
    body = d3.select('body')
    body.append('div').attr('class','paragraphs_container')
    d3.selectAll('.paragraphs_container')
        .selectAll('p')
        .data(tweet_data)
        .enter()
        .append('p')
        .attr('class', 'handle')
    handles = d3.selectAll('.handle')
        .text(function(d){
            return d.actor.preferredUsername}) 
}
</pre>

Now call that function:   
`displayhandles()`

Awesome! What did we do?

`body = d3.select('body')` selects an html element to append children to.  

Here's where the magic happens:
`body.append('div').attr('class', 'paragraph_container')` creates and classes a new `div` where we will put our new paragraphs. creating a new div for a new set of objects makes selecting all of the paragraphs we want to deal with easier, without accidentally selecting unrelated pieces of our DOM
`d3.selectAll(.paragraph_container')` selects all of the elements that we are going to want to append data to (in this case, there aren't any 'p' elements in this div just yet, but we are setting up a selecting that will contain all 'p' elements in the div)
`.data(tweet_data)` selects all of the data we are going to associate with elements   
`.enter()` creates a new element for each datum for which there is not already an element. magic, right there.    
`.append('p')` makes a new element for each entered thing    
`.attr('class', 'handle')` classes the objects that we just made    
Then:
`d3.selectAll('.handle')` makes a selection of all of the handle objects    
`.text(...)` gives them a text attribute based on thier data. Great!    

Now, inside of displayhandles() we definied a global variable `handles` which contains that selection. Look at 'handles' in your console, and notice a few things: it's an array of `p.handle` objects, each `p.handle` thing has a `_data_` attribute wrapped up in it that contains the tweet (datum) associated with the object. It's important to note that this `_data_` attribute is persistant, it remains associated with whatever thing you created and bound to your data. Each object in this selection also contains all kinds of other attributes associated with paragraph objects--you can find the attributes that you set, such as "textContent" and "className", as well as a lot of other information that you have not set explicitly, but could.


## Example
Many of these concepts are tied up in an example in tweet_bars.html, which is included in the repo. You can give it a look to see data binding in action, as well as scales, shapes (which we haven't discussed yet).
To look at tweet_bars.html, replace `hello-d3.html` in your browser with `tweet_example/tweet_bars.html`. View the source and comments to get an idea of what the code is doing, and inspect variables like `handles` to look at a d3 selection of svg text objects--you'll notice many of the same properties that `handles` had in the previous example.
