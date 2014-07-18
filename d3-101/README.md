D3 101
---------
---------
[cheat sheet](https://github.com/alignedleft/strata-d3-tutorial/blob/master/d3%20Cheat%20Sheet.pdf)

# Javascript intro
Let's start by opening a blank template. Follow these instructions in [Chrome](https://www.google.com/intl/en/chrome/browser/#brand=CHMB&utm_campaign=en&utm_source=en-ha-na-us-sk&utm_medium=ha) browser. 

*  click [here](http://data-science-6.gnip.com/~blehman/hello-d3.html) and open the link in Chrome. 

*  Press `option+command+j`. 


Inside the developer window we can select `Elements` tab to view the structure of the [dom](http://en.wikipedia.org/wiki/Document_Object_Model). The `body` element contains some script (`<script> </script>`) and a paragraph (`<p> </p>`). The script that allows us to access the d3 library is highlighted below.  

![](https://github.com/blehman/Data-Science-45min-Intros/blob/master/d3-101/imgs/elements.png?raw=true)

Notice that below the `Network` tab, we can select a `Console` subtab. There's also a parent  `Console` tab. Either works for typing commands. We can now type javascript and d3 commands directly in the console.

![](https://github.com/blehman/Data-Science-45min-Intros/blob/master/d3-101/imgs/console.png?raw=true)

### Array
The javascript `array` is like a python `list`.

####assignment
<pre>
my_array=['bob',5];

console.log(my_array);

my_array[2]="WEE"

console.log(my_array);

my_arry.pop() <removes the last element>

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
    `alert(obj.obj_keys[i]);`
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

#D3
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

## Scales & Axes

## Shapes

