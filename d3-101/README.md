D3 101
---------
---------
[cheat sheet](https://github.com/alignedleft/strata-d3-tutorial/blob/master/d3%20Cheat%20Sheet.pdf)

## Javascript intro
Javascript is a neat, lecically scoped language.

### javascript `array` is python `list`

####assignment
my_array=['bob',5];

my_array[2]="WEE"

my_arry.pop() <removes the last element>

my_array.push("lucy") <adds element to last>

my_array.splice(0,2) <removes 2 elements starting at 0>


####iterate
my_array.forEach(function(d,i,a){ console.log(d)})

for (var i = 0; i < my_array.length; i++) {
    alert(my_array[i]);
}

### javascript `object` is python `dict`

####assignment
obj = {"name":"bob","age":5};

####read
keys(obj)
values(obj)

####assignment
obj.gender='male'
obj['income']="$2"

delete obj['income'] 
delete obj.gender

####iterate
obj_keys=keys(obj)
for (var i = 0; i < obj_keys.length; i++) {
    alert(obj.obj_keys[i]);
}

### Scope
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


## Selections
Let's start by opening a blank template [here](http://data-science-6.gnip.com/~blehman/hello-d3.html). Press `option+command+j` and then type the following in the console:

`d3.append('p')` 

You receive a type error because you haven't selected anything to which you can append a paragraph. Now try the following:

`d3.select('body').append('p').text("Look, I made a paragraph!")`

d3.select('body').append('div').append('p').attr('class',"BEST_P_EVER")
d3.select(".BEST_P_EVER").text('Hello world.')
d3.select(".BEST_P_EVER").style('color','blue') <style overides css style>


Selections are arrays.

\#foo        // `<any id="foo">`  
foo         // `<foo>`  
.foo        // `<any class="foo">`  
[foo=bar]   // `<any foo="bar">`   
foo bar     // `<foo><bar></foo>`  
foo.bar     // `<foo class="bar">`  
foo\#bar     // `<foo id="bar">`  

Chaining can simplify code. 

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
function displayhandles(){
    body = d3.select('body')
    body.select('p').data(tweet_data).enter().append('p').attr('class', 'handle')
    d3.selectAll('.handle').text(function(d){
        return d.actor.preferredUsername}) 
}

Now call that function:   
`displayhandles()`

Awesome!






## Scales & Axes

## Shapes

