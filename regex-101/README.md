
built on Ubuntu 12.04

don't be redundant here, so keep it short > something about context of using GNU ``grep -e`` as the "platform" for testing regular expressions, but generally applicable to Python, vim, ``sed``, ..., though each has it's subtlties and additional features.

note about extra features of -e, specifically OR
 

refs:
- [zytrax](http://www.zytrax.com/tech/web/regex.htm)
- [TLDP](http://www.tldp.org/LDP/abs/html/x17129.html)

Bad example, but impressive: [RFC822 email validation regular expression](http://www.ex-parrot.com/pdw/Mail-RFC822-Address.html). Here's
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

work on a data science server so we're all using the same settings / environments

    wget (dropbox link for poolboy code)

### terminology

*literal* - a character used to match in a search e.g. the ``a`` in ``bat``, or the ``og`` in ``dog`` can both be considered literal strings

*metacharacters* - (includes *anchors* that deal with line position; and *modifiers* that modify the range, e.g ``*``, ``[``, ``]``, ``\]`` 

*target string* - string to be searched for the pattern

*escape sequence* - combination of escape metacharacter ``\`` and literal(s). each metacharacter desired to be treated as a literal gets escaped


### context

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


## simple matching

Some simple literal character matching examples. Have a look at the ``small.log`` file, and check that the matching makes sense. 

    $ grep -e"DEBUG" small.log 
    $ grep -e"20:59:22" small.log
    $ grep -e"]" small.log
    $ grep -e"[" small.log          # note the difference; [ is a metacharacter! (more to come below) 
    $ grep -e"1>" small.log


## metacharacters

### brackets, ranges, negation

For these examples, really take a second to really analyze the resulting match, so the pattern matching concepts become as clear as possible. Some of them are subtle!

``[ ]`` - (L and R square brackets) used together and denote a list of characters to match against each character position in the target (once and only once). 

    $ grep -e"[01]" small.log

``-`` - (dash) within brackets, specifies a range of characters to match against the target (there are additional "[special ranges](http://www.zytrax.com/tech/web/regex.htm#special)" that may (or may not) be available on your system). The next three lines should all return the same matches: 

    $ grep -e"[0123456789]" small.log
    $ grep -e"[0-9]" small.log              # (I think this one is the most intelligible)
    $ grep -e"[[:digit:]]" small.log

    $ grep -e"[a-z]" small.log              # note the differences b/w these three
    $ grep -e"[A-Z]" small.log
    $ grep -e"[a-Z]" small.log

    $ grep -e"[0-9]]" small.log             # R square bracket is now *outside* the range character, so it's literal
    $ grep -e"[0-9\]]" small.log            # same matches as ^, but *not* identical pattern -- can you see why? 

``^`` - (caret / circumflex) *within* brackets, negates the expression 

    $ grep -e"[^a-m]" small.log
    $ grep -e"[^a-m0-5]k" small.log         # combined range (*for a single character match*) is specified 
                                            #   w/o spaces 
                                            # --note: this range matches any *one* character that is not in 
                                            #   a-m *or* any digit not in 0-5. not one followed by the other. 

### anchors 

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


### iteration / repetition

*note about greedy matching*

To control the *number of times* a character is matched, it should be followed by an iteration (or repetition) metacharacter. Note that the output coloring for matched patterns is off for this section. Pay attention to the lines returned by ``grep`` rather than the characters that it highlights in the output.

``*`` - the asterisk matches *0 or more* occurrences of the preceding character

    $ grep "0*" small.log 
    $ grep "s.*D" small.log

``+`` = the plus sign matches *1 or more* occurrences of the preceding character

NB: the ``+`` metacharacter (along with ``?``, ``+``, ``{``, ``|``, ``(``, ``)`` ) lose their special meaning in *basic* regular expressions e.g. the default behavior of ``$ grep PATTERN FILE``. In order to use these as iteration metacharacters in the context of basic ``grep``, they must be escaped. Alternatively, ``grep`` can be called in *extended* regular expression mode with the ``-E`` option: ``$ grep -E PATTERN FILE`` (there was once an ``egrep`` command that was synonymous but is deprecated).  

    $ grep "0+" small.log                   # matches a literal 0 followed by a literal +
    $ grep "0\+" small.log                  # + becomes iteration metachar
    $ grep -E "0+" small.log                # equivalent pattern to ^
    
``?`` - the question mark matches *0 or 1* occurrences of the preceding character 

    come back to this one - not getting to behave as expected (greedy?) 

*[ WIP ]*

``{ }`` - the curly brackets specify a count or a range or occurences to match the preceding pattern. If used with a single number eg ``{n}``, pattern matches preceding character exactly ``n`` times. With a range eg ``{n,m}``, pattern matches at least ``n`` times, but not more than ``m`` times. With a single number + comma eg ``{n,}``, pattern matches preceding character at least ``n`` times

    $ grep "15\{2\}1" small.log
    $ grep -E "15{2}1" small.log
    $ grep -E "15{1,2}1" small.log
    $ grep -E "15{2,}1" small.log 
 

### grouping and OR-ing (alternation)

*[ WIP ]*






## appendix

- backreferences
- more character classes
- submatches / subexpressions
- ``grep`` vs. ``egrep`` vs. ``fgrep`` 






footnote:

note about parsing html with regex [SO link](http://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags/1732454?stw=2#1732454)



