
built on Ubuntu 12.04

refs:
    - [zytrax](http://www.zytrax.com/tech/web/regex.htm)
    - [TLDP](http://www.tldp.org/LDP/abs/html/x17129.html)


[RFC822 email regexp validation](http://www.ex-parrot.com/pdw/Mail-RFC822-Address.html). Here's
the first few lines:

    (?:(?:\r\n)?[ \t])*(?:(?:(?:[^()<>@,;:\\".\[\] \000-\031]+(?:(?:(?:\r\n)?[ \t]
    )+|\Z|(?=[\["()<>@,;:\\".\[\]]))|"(?:[^\"\r\\]|\\.|(?:(?:\r\n)?[ \t]))*"(?:(?:
    \r\n)?[ \t])*)(?:\.(?:(?:\r\n)?[ \t])*(?:[^()<>@,;:\\".\[\] \000-\031]+(?:(?:(
    ?:\r\n)?[ \t])+|\Z|(?=[\["()<>@,;:\\".\[\]]))|"(?:[^\"\r\\]|\\.|(?:(?:\r\n)?[ 
    \t]))*"(?:(?:\r\n)?[ \t])*))*@(?:(?:\r\n)?[ \t])*(?:[^()<>@,;:\\".\[\] \000-\0
    31]+(?:(?:(?:\r\n)?[ \t])+|\Z|(?=[\["()<>@,;:\\".\[\]]))|\[([^\[\]\r\\]|\\.)*\
    ](?:(?:\r\n)?[ \t])*)(?:\.(?:(?:\r\n)?[ \t])*(?:[^()<>@,;:\\".\[\] \000-\031]+
    ...


### background

RE v. ERE (de facto standard) now


### setup notes 

    wget (dropbox link for poolboy code)
    set up colorful grep / work on DS server


### terminology

``literal`` - a character used to match in a search e.g. the ``a`` in ``bat``, or the ``og`` in ``dog`` can both be considered literal strings

``metacharacters`` - (includes ``anchors`` [line position] and ``modifiers`` [modify the range, e.g ``*``, ``[``, ``]``, ``\]``] 

``target string`` - string to be searched for the pattern

``escape sequence`` - combination of escape metacharacter ``\`` and literal(s). each metacharacter desired to be treated as a literal gets escaped


### contexts

*lots* of overlap, but subtle differences between the various places you can match patterns with a regular expression: 

- shell commands (eg. GNU ``grep``, ``sed``) 

- vi(m) 

- Python  

We'll use the GNU ``grep`` for our examples. This is nice because it allows for multiple expressions. From the ``grep`` docs:

    grep [OPTIONS] [-e PATTERN | -f FILE] [FILE...]
    ...
    -e PATTERN, --regexp=PATTERN
                  Use PATTERN as the pattern.  This can be used to specify multiple search patterns, or to protect a pattern beginning with a hyphen (-).  (-e is specified by
                  POSIX.)
    ...


### simple matching

Some simple matching examples. Have a look at the ``small.log`` file, and check that the matching makes sense. 

    $ grep -e"DEBUG" small.log 
    $ grep -e"20:59:22" small.log
    $ grep -e"]" small.log
    $ grep -e"[" small.log          # note the difference here! [ is a metacharacter unless it's escaped (more to come below) 
    $ grep -e"1>" small.log


## metacharacters

### brackets, ranges, negation

``[ ]`` - (L and R square brackets) used together and denote a list of characters to match against each character position in the target (once and only once). 

    $ grep -e"[01]" small.log

``-`` - (dash) within brackets, specifies a range of characters to match against the target (there are additional "[special ranges](http://www.zytrax.com/tech/web/regex.htm#special)" that may (or may not) be available on your system). The following should all return the same matches: 

    $ grep -e"[0123456789]" small.log
    $ grep -e"[0-9]" small.log              # (I think this one is the most intelligible)
    $ grep -e"[[:digit:]]" small.log

    $ grep -e"[a-z]" small.log              # note the differences b/w these three
    $ grep -e"[A-Z]" small.log
    $ grep -e"[a-Z]" small.log

    $ grep -e"[0-9]]" small.log             # R square bracket is now outside the range, so it is literal

``^`` - (caret / circumflex) within brackets, *negates* the expression 

    $ grep -e"[^a-m]" small.log
    $ grep -e"[^a-m0-5]k" small.log         # combined range is specified w/o spaces 











