# Regex 101: Building Blocks 

Josh Montague, 2014-05-23

### Build notes

These examples were designed using ``grep`` 2.10 and ``sed`` 4.2.1 on Ubuntu 12.04. If using something else (especially OS X), ymmv. This walk-through assumes approximately zero previous knowledge of regular expressions or command line tools like ``grep``, or ``sed``. We'll use them to learn stuff, but you can read the ``man`` pages for more intimate details on how they work. 

## Background

There are many places to use regular expressions ("regex"). Most environments and programs (Python, vim, \*sh commands like ``grep``, ...) include the concept, but may introduce subtlties in the handling of expressions (paricularly escaping characters). For consistency, we're going to use ``grep`` for most of our regex pattern matching. This approach is pretty readable which is a win: ``$ grep "[PATTERN]" [FILE]``. 

Following the [Zed Shaw](http://learncodethehardway.org/) philosophy of learning, you're advised to actually smash your fingers onto the appropriate keys to recreate the examples here. And though we'll cruise through this the first time, revisit it occasionally for ideal retention. 

Use this __Hack Button__ [![Hack DrSkippy/Data-Science-45min-Intros.git directly on Nitrous.IO](https://d3o0mnbgv6k92a.cloudfront.net/assets/hack-s-v1-7475db0cf93fe5d1e29420c928ebc614.png)](https://www.nitrous.io/hack_button?source=embed&runtime=nodejs&repo=DrSkippy%2FData-Science-45min-Intros.git&file_to_open=regex-101%2FREADME.md) to access a Linux instance with grep and sed already loaded and ready to go!


### Start with the bad news

Though extremely powerful, regular expressions ("regex") can be ungodly awful to read. Regex is a mighty sword that can also be wielded for evil. Here's an example; these are the first few lines of the famous [RFC822 email validation regular expression](http://www.ex-parrot.com/pdw/Mail-RFC822-Address.html) (check the link to see the whole thing): 

    (?:(?:\r\n)?[ \t])*(?:(?:(?:[^()<>@,;:\\".\[\] \000-\031]+(?:(?:(?:\r\n)?[ \t]
    )+|\Z|(?=[\["()<>@,;:\\".\[\]]))|"(?:[^\"\r\\]|\\.|(?:(?:\r\n)?[ \t]))*"(?:(?:
    \r\n)?[ \t])*)(?:\.(?:(?:\r\n)?[ \t])*(?:[^()<>@,;:\\".\[\] \000-\031]+(?:(?:(
    ?:\r\n)?[ \t])+|\Z|(?=[\["()<>@,;:\\".\[\]]))|"(?:[^\"\r\\]|\\.|(?:(?:\r\n)?[ 
    \t]))*"(?:(?:\r\n)?[ \t])*))*@(?:(?:\r\n)?[ \t])*(?:[^()<>@,;:\\".\[\] \000-\0
    31]+(?:(?:(?:\r\n)?[ \t])+|\Z|(?=[\["()<>@,;:\\".\[\]]))|\[([^\[\]\r\\]|\\.)*\
    ](?:(?:\r\n)?[ \t])*)(?:\.(?:(?:\r\n)?[ \t])*(?:[^()<>@,;:\\".\[\] \000-\031]+
    ...

This is basically a crime against humanity in terms of the [Unix philosophy](http://en.wikipedia.org/wiki/Unix_philosophy). By continuously appending edge cases to this regex, it's now completely intractable. However, when used with care, tiny pieces of regex are incredibly powerful. Below is an introduction to some of the fundamental units of a regex. The beauty of the regex is that once you learn the building blocks, you can combine them in infinitely-extensible ways. Just don't build a single-expression, 100-line email address parser, please. 


### Vocabulary 

*literal*: a character used to match in a search e.g. the ``a`` in ``bat``, or the ``og`` in ``dog`` can both be considered literal strings

*metacharacters*: *anchors* that deal with line position, and *modifiers* that deal with counting and specifying ranges, e.g ``*``, ``[``, ``]``. 

*target string*: string to be searched by the pattern

*escape sequence*: combination of escape metacharacter ``\`` and literal(s). Each metacharacter desired to be treated as a literal gets escaped


## Simple matching

Some simple literal character matching examples. Have a look at the ``small.log`` file, and check that the matching makes sense. 

    $ grep "DEBUG" small.log 
    $ grep "20:59:22" small.log
    $ grep "]" small.log
    $ grep "[" small.log          # note the difference; [ is a metacharacter! (more to come below) 
    $ grep "1>" small.log


## Metacharacters

### Brackets, ranges, negation

For these examples, really take a second to really analyze the resulting match, so the pattern matching concepts become as clear as possible. Some of them are subtle!

``[ ]`` - (L and R square brackets) used together and denote a list of characters to match against each character position in the target (once and only once). 

    $ grep "[01]" small.log

``-`` - (dash) within brackets, specifies a range of characters to match against the target (there are additional "[special ranges](http://www.zytrax.com/tech/web/regex.htm#special)" that may (or may not) be available on your system). The next three lines should all return the same matches: 

    $ grep "[0123456789]" small.log
    $ grep "[0-9]" small.log              # (I think this one is the most intelligible)
    $ grep "[[:digit:]]" small.log

    $ grep "[a-z]" small.log              # note the differences b/w these three
    $ grep "[A-Z]" small.log
    $ grep "[a-Z]" small.log

    $ grep "[0-9]]" small.log             # R square bracket is now *outside* the range character, so it's literal
    $ grep "[0-9\]]" small.log            # same matches as ^, but *not* identical pattern -- can you see why? 

``^`` - (caret / circumflex) *within* brackets, negates the expression 

    $ grep "[^a-m]" small.log
    $ grep "[^a-m0-5]k" small.log         # combined range (*for a single character match*) is specified 
                                            #   w/o spaces 
                                            # --note: this range matches any *one* character that is not in 
                                            #   a-m *or* any digit not in 0-5. not one followed by the other. 

### Anchors 

When you need to make your match pattern include physical positions within the line, we can use the following three characters:

``^`` - the caret makes an encore appearance, but this time it is *outside* of the square brackets introduced above for denoting a list of characters. In this context, it refers to the *beginning* of the line. 

    $ grep "^\[" small.log                  # [ is a metacharacter
    $ grep "^[^[]" small.log                # "opposite" of the previous pattern
    $ grep "^[^[:punct:]]" small.log

``$`` - the dollar sign means the *end* of the line

    $ grep "[0-9]$" small.log
    $ grep "[a-Z]$" small.log

``.`` - the period refers to *any* one character in a position 

    $ grep "E.U" small.log 
    $ grep "m.p" small.log
    $ grep "m\.p" small.log                 # what's the difference b/w this pattern & the previous one? 

See also: ``\<``, ``\>``, ``\b``


### Iteration / repetition

To control the *number of times* a character is matched, it should be followed by an iteration (or repetition) metacharacter. Note that the output coloring for matched patterns is off for this section. Pay attention to the lines returned by ``grep`` rather than the characters that it highlights in the output.

``*`` - the asterisk matches *0 or more* occurrences of the preceding character

    $ grep "0*" small.log 
    $ grep "s.*D" small.log

``+`` - the plus sign matches *1 or more* occurrences of the preceding character

NB: the ``+`` metacharacters (and, really, the whole set: ``?``, ``+``, ``{``, ``|``, ``(``, ``)`` ) lose their special meaning in *basic* regular expressions e.g. the default behavior of ``$ grep PATTERN FILE``. In order to use these as iteration metacharacters in the context of basic ``grep``, they must be escaped. Alternatively, ``grep`` can be called in *extended* regular expression mode with the ``-E`` option: ``$ grep -E PATTERN FILE`` (there was once an ``egrep`` command that was synonymous but is deprecated).  

    $ grep "0+" small.log                   # matches a literal 0 followed by a literal +
    $ grep "0\+" small.log                  # + becomes iteration metachar
    $ grep -E "0+" small.log                # equivalent pattern to ^
    
``?`` - the question mark matches *0 or 1* occurrences of the preceding character 

    $ grep -E "15?1" small.log              # (note about my confusion here)
    $ grep -E "colou?r" small.log           # English spelling check

``{ }`` - the curly brackets specify a count or a range or occurences to match the preceding pattern. If used with a single number eg ``{n}``, pattern matches preceding character exactly ``n`` times. With a range eg ``{n,m}``, pattern matches at least ``n`` times, but not more than ``m`` times. With a single number + comma eg ``{n,}``, pattern matches preceding character at least ``n`` times

    $ grep "15\{2\}1" small.log
    $ grep -E "15{2}1" small.log
    $ grep -E "15{1,2}1" small.log
    $ grep -E "15{2,}1" small.log 
 

### Grouping 

*Change-up!*

So far, we've been using ``grep`` as a way to both match regex and, conveniently (most of the time), highlight the matches thanks to the default Ubuntu ``.bashrc`` settings. ``grep`` is fundamentally about matching pattern and returning the matching *lines*. What we're about to work through is a little more subtle and is better suited for demonstration with ``sed`` than ``grep``. Thankfully, we're working on a beautiful Linux system that has both of these ready to rock. If you want to, you can go ahead and read the ``man`` page for ``sed``, but for the sake of this little demonstration, all you need to know is the following syntax:

    $ sed 's/[REGEX PATTERN]/[REPLACEMENT PATTERN]/g' FILE 

``sed``'s ``s/thing1/thing2/g`` pattern is often used to search for ``thing1`` and replace it with ``thing2`` (everywhere, in this case). So we'll continue to use small.log as our ``FILE`` and we'll explore the results of our regex by adding the pattern between the first two slashes, and then selecting groups (or subexpressions) into the replacement pattern (between the second and third slashes). A quick example to make the use of ``sed`` super clear:

    $ sed 's/[0-9]/Q/g' small.log 

One unfortunate gotcha: ``sed`` - like just about every environment where you want to use regex - has it's own rules about escaping. The escape character is still ``\`` but you may need to use one where you didn't have to in the previous ``grep`` examples. The example below illustrates this.

``( )`` - the open and close parantheses ("parens") group parts of the expression into subexpressions (or submatches, or groups). Awesomely, these matches are actually captured into variables so you can reuse them. This is called back-referencing, and the variables are accessed via ``\N`` where ``N`` is the numbered order of the matching subexpression (1, 2, ...). 

To be slightly more explicit, I'll build up to this example. The mission is as follows: 

> You have a log file where the dates were stored in ``yyyy-mm-dd`` format. You needed them to be in ``dd-mm-yyyy`` format using only your shell command line tools.

Recall the grep approach to capturing a certain number of characters that match a range:

    [0-9]{4}                      # matches four digits in a row 
    [0-9]{4}-[0-9]{2}-[0-9]{2}    # matches a typical date format

Now we want to group each set of numbers into a subexpression so we have access to the year, month, and day in separate variables. Remember to escape the parens:

    \([0-9]{4}\)-\([0-9]{2}\)-\([0-9]{2}\)    

When this matches a valid date, ``\1`` stores the year, ``\2`` the month, and ``\3`` the day the line above is *almost* our finished regex, which we can drop into the ``sed`` command. The only remaining sadness is that the curly brackets need to be escaped within a ``sed`` expression. Escaping makes for a sad panda

    \([0-9]\{4\}\)-\([0-9]\{2\}\)-\([0-9]\{2\}\)

Now drop this regex into the ``sed`` expression and use back-references to change the order. Don't forget to put the hyphens back in, too!

    $ sed 's/\([0-9]\{4\}\)-\([0-9]\{2\}\)-\([0-9]\{2\}\)/\3-\2-\1/g' small.log     # BOOM

Yes, the escaping is terrible. But once you do it a bit, you start to see through the escaping and identify the underlying structures: the groups, the ranges, the anchors, etc. Sad panda is sad, but sad panda is very powerful. 

![powerful panda](./panda.jpg "escaping. deal with it.")


### OR-ing (alternation)

*Back to ``grep``!*

``|`` - the pipe (or vertical bar) is an "or" and "alternation" and will match either the expression on the left or right side of the symbol. This can be combined with parens within a character string, or also used to OR entire expressions.

    $ grep "05\|22" small.log 
    $ grep -E "[0-9]{8}|[a-Z]{10}" small.log    # recall -E escaping 
    $ grep -E "o(l|r)" small.log
    $ grep "o\(l\|r\)" small.log


*the end*

-------

### Notes 

There are a lot of avenues to further explore the capabilities of regular expressions. We covered most of the building blocks, but here are a handful of possible next steps and assorted other notes to learn from while you're waiting for the 201 session of the class: 

I used these two resources for getting this outline laid out. The TLDP link has far more than is possible to fit in a 101 class: 
- [zytrax](http://www.zytrax.com/tech/web/regex.htm)
- [TLDP](http://www.tldp.org/LDP/abs/html/x17129.html)

Some other assorted things if you're interested in taking all of this a few steps further:

**backreferences**
- there are even more ways to use these... for example, define a group so that you can reuse that group in your *matching expression* instead of just the result. 

**more character classes**
- there are other [character classes](http://www.zytrax.com/tech/web/regex.htm#special) that I didn't mention. 

**``grep`` vs. ``egrep`` vs. ``fgrep``** 
- Though ``egrep`` is deprecated, it is the same as using ``grep -E``. This extends ``grep`` to "extended ``grep``". Additionally, there is ``grep -F`` which does not evaluate the expression being used for matching. That is, if you're searching for plain text (literal characters), ``fgrep`` should be faster to finish searching and possibly matching. 

**don't reinvent the wheel**
- for commonly-used pattern matching, there are [inventories](http://regexlib.com/DisplayPatterns.aspx) of expressions to use

**don't use regex for all of your parsing**
- particularly, don't try to [parse HTML](http://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags/1732454?stw=2#1732454)



