D3 101
---------
---------
[cheat sheet](https://github.com/alignedleft/strata-d3-tutorial/blob/master/d3%20Cheat%20Sheet.pdf)

## Javascript intro

### Variable assignment 

### logical operands

### Traverse array [...]

### Traverse object {...}

## Selections
Let's start by opening a blank template [here](http://data-science-6.gnip.com/~blehman/hello-d3.html). Press `option+command+j` and then type the following in the console:

`d3.append('p')` 

You receive a type error because you haven't selected anything to which you can append a paragraph. Now try the following:

`d3.select('body').append('p').text("Look, I made a paragraph!")`

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

## Scales & Axes

## Shapes

