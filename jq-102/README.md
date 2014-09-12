# A Brief Introduction to jq

jq has been referred to as "sed for JSON data." Like sed, it provides functionality around
the filtering of the data, the editing of the data, and the construction and insertion of new data. 
The manual can be found [here](http://stedolan.github.io/jq/manual/).

# Building blocks of jq

A call to jq typically takes the form `jq 'FILTER_1 | FILTER_2 | FILTER_N' < input_file.json`.
Lines consisting of JSON-formated strings are recieved from stdin. Output in the form of whitespace-separated,
JSON-formatted strings is sent to stdout. jq provides a variety of command line options to select
other input and output preferences. These are well-documented in the manual.
The filters themselves are constructed from keys and indicies that refer to specific elements of the JSON data types,
as well as jq-specific functions and keywords. 

Things to note:

* Everything goes into single quotes, so as to not confuse the shell.
* The pipe character (inside the single quotes) is NOT a shell pipe, but it _does_ have similar behavior.
* jq defines a null object, which is created by erroneous requests. It has zero length, 
and is interpreted by the shell as a blank line. There are options to change this behavior.
* Output is "prettified" by default.

## JSON data types

* bool/number/string/null
* array - ordered sequence of zero or more values (AKA list)
* object - unordered sequence of key:value pairs (AKA dictionary, associative array, map)

## Single filter operations

`.` : the simplest operation, which just prints the input data. The dot must start any filter expression
that acts on the input data.

`NUM` : ignores the input and output NUM, where NUM can be any data

`.KEY` : acts on an object, returning the value associated with key KEY

`.KEY_1.KEY_2` : acts on an object; if `.KEY_1` returns another objects which contains key KEY\_2, 
it returns the value associated with KEY\_2

`.[X:Y]` : acts on an array; returns a slice from index X through index Y

`.[]` : acts on an array; returns all elements sequentially

It's helpful to remind oneself of the input and output type for each filter.

## Combination and control

Much like a standard UNIX tool like `sed`, jq acts sequentially on a stream of newline-separated, JSON-formatted string. 
Within jq, however, it is possible for a filter to output more than one result. 
These results are treated sequentially by the next filter. 
However, unlike lines from stdin, they can be joined again by downstream filters.

`?` The question mark placed after a filter supresses errors due to non-extistent keys or indicies. 
However, this seems to have a version dependancy.

`FILTER_1,FILTER_2` The comma is placed between two filters, both of which act independantly on the input.
The output from the filters is passed on sequentially: first the output from FILTER\_1, then the output from FILTER\_2.

`FILTER_1 OPER FILTER_2` The operator `OPER` acts on the outpus of FILTER\_1 and FILTER\_2,
producing a result that is appropriate to the output data types. If `OPER` is `+` or `-`,
it can act on any data types. If `OPER` is `/`, `*`, or `%`, it will only act on numbers.

## Data construction

`[FILTER_1,FILTER_2]` : returns an array containing the outputs of the filters

`{FILTER_1,FILTER_2}` : returns an object with key,value pair given by the outputs of FILTER\_1 and FILTER\_2

## Conditional statements

Conditional statements return boolean values, which are often passed as arguments to functions. 
Conditional statements take the form `FILTER_1 COND_OPER FILTER_2`, where COND\_OPER is one of `==`,`!=`,`>`,`<`,`>=`,or `<=`.

# Examples 

## An array example to demonstrate the difference between "|" and "."

Start by getting the Klout topics array:

```
cat tweet2.json | jq '.gnip.klout_profile.topics'
```

The key names are separated by dots because this is a straightforward "drill down" through the tweet structure. 
To dig further, we need to select an element or elements of the array.

```
cat tweet2.json | jq '.gnip.klout_profile.topics[0].displayName'
```

Because the array index operator "[]" returns an object, it can be immediately followed with a dot and a keyword.
However, the "[]" operator is not preceeded by a dot, because "[0]" is not a valid key
(and the output of .topics isn't an object anyway).

The `map` function acts on an array, applies a filter to each element, and returns the results as an array.
However, we need a new filter to use `map`.

```
cat tweet2.json | jq '.gnip.klout_profile.topics | map(.link)'
```

This same operation can be applied to a list of tweets. 

```
cat tweets.json | jq '.gnip.klout_profile.topics | map(.link)'
```

I leave the error handling of empty arrays as an exercise to the reader.

## Get (username, Klout score) pairs

Getting the username and Klout scores individually is easy.

```
cat tweets.json | jq '.actor.displayName'
```

```
cat tweets.json | jq '.gnip.klout_score'
```

It's also easy to print them together, but the comma construction returns them on separate lines.

```
cat tweets.json | jq '.actor.displayName, .gnip.klout_score'
```

Solution: use the "join" function, after casting the Klout score to the same data type as the username,
and putting the items in an array. 

```
cat tweets.json | jq '[.actor.displayName, .gnip.klout_score|tostring]|join(", ")'
```

Another solution uses the "add" function:

```
cat tweets.json | jq '[.actor.displayName, .gnip.klout_score|tostring]|add'
```

## For a top-n list, get (count n, item n) pairs

Start by looking at the data:

```
cat top_n.json | jq '.'
```

Extract the 'data' element:

```
cat top_n.json | jq '.data'
```

It's an array. To print attributes of the array elements, we use the "[]" operator on an array to pass on each array element as a separate item:

```
cat top_n.json | jq '.data[].key'
```

or

```
cat top_n.json | jq '.data| .[].key'
```

We can additionally use the slice notation, but we still need to "[]" operator to decompose the array:

```
cat top_n.json | jq '.data[0:10][].key'
```

Note that we can combine the array decomposition operator with the "key" selection, because the operator is returning individual items that have keys named "key".

Since the top-n are ordered, we can now extract the "value" items. 

```
cat top_n.json | jq '.data[0:10][].value'
```

Hm...looks like we have a proble: we need to get the counts and the terms on the same line. 
The trick is to select items according to a condition. This will require two new function: `select` and `contains`.

```
cat top_n.json | jq '.data[0:10][] | select("lala"|contains("la"))'
```

The `select` function operates on each object returned by the array decomposition, and since "lala" always contains "la",
all objects are passed on to the output unchanged. Let's now make a meaninful selection on the key of the object, but return its value.

```
cat top_n.json | jq '.data[0:10][] | select(.key|contains("count")).value'
```

We know the trick from the previous example to get items side-by-side. Let's do that for the count and term values, remembering to cast.

```
cat top_n.json | jq '.data[0:10][] | select(.key|contains("count")).value, select(.key|contains("item")).value'
```

Here, a little awk statement joins  pairs of lines nicely...

```
cat top_n.json | jq '.data[0:10][] | select(.key|contains("count")).value, select(.key|contains("item")).value' | awk '{a=$0; getline; print a ", " $0}'
```

And now for the the entire top-5000:

```
cat top_n.json | jq '.data[] | select(.key|contains("count")).value, select(.key|contains("item")).value' | awk '{a=$0; getline; print a ", " $0}'
```

# Some notes

A few commands don't work as advertized in the manual, despite having the most recent version of jq.

* `sort`
* `?`
* `group`
* `flatten`
