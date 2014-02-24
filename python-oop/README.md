# OOP in Python (with a dash of packaging)

A short overview illustrating some aspects of Object Oriented Programming (OOP) in Python including: classes, functions, methods, inheritance. And, while we're at it, some discussion of modules and packages. 

Built on Python 2.7.6, but should work just fine on 2.x

Much of this walk-through will involve some learning about modules and packages in Python, so here are some great reference materials (to both have open and bookmarked for later):

- [Introduction to Modules](http://docs.python.org/2/tutorial/modules.html) from official Python tutorial

- [Introduction to Packages](http://www.network-theory.co.uk/docs/pytut/Packages.html) from the creator, himself

There are a lot of words in this README. Sorry about that. This was my attempt to lay things out logically for presentation, but hopefully you can also just read through them and get the gist.

---------

## The Transcript 

We'll start simply and build up in complexity. My goal is for you start by being bored, and then have you gain traction along the way as learn something new.  



### Script 

First, look at the data file. Should look like standard `gnacs`-ified Twitter Activity Streams. No surprises up that sleeve.

Start with an example of the simple Python script functionality with which many folks (myself included) begin using Python. Send some data to the shell's `stdout` and read / do something with it via `sys.stdin` in our Python code. Run the data through the script first, and then we'll dive deeper:  

    $ cat data.csv | ./simple_script.py     # ideally, you get something like this... 
    line number: 0, tweet body: kavga edelim ama konuşalım
    line number: 1, tweet body: @shane_joersz wooooow
    line number: 2, tweet body: お前との肌のふれあいなんぞ求めてない。自重しろ。
    line number: 3, tweet body: @Gabo_navoficial yo tambien creo en ti mi charro bello:))
    line number: 4, tweet body: только ты об этом не знаешь... http://t.co/MOH8pcKyJY

Now, let's look at the code in `simple_script.py`. If you're coming from another OO language, your first inclination may be to seek out things that match the pattern ``A.B``. In many OO languages, this suggests that ``A`` is an object and ``B`` is something defined within the scope of that object e.g. a method or attribute. The same is true in Python, only it has a subtle variations when it comes to modules and packages. On line 7 we import the standard-library module ``sys`` (ie. no ``pip install``, it came built-in). On line 10, we write a version of the most common Python scripting line ever written: ``for line in sys.stdin: ....``. Here, we use dot notation reach into the ``sys`` module and address an attribute defined therein, the ``stdin`` file object. 

It's not quite as obvious an implementation of object creation as ``thing = NewThing()`` followed by ``thing.method()`` (if that comparison doesn't make sense yet, hold tight... we're getting there). But, the ``import useful-module`` statement does actually instantiate an object that lets you use it later on. Ok, so let's just let that simmer for a bit. In line 10 we make use ``stdin`` file object to buffer lines from the shell and we've also done two other object creation steps: created an integer called ``cnt`` and a string object ``line``. As a result, we can use all of the methods and attributes that belong to these variables, which we quickly do: in line 11, we use the ``split()`` method, which is defined in the string class. This one line actually has another object-specific attribute use: ``split()`` returns an object of type list, and we use the ability to index the items in that list to extract the thing we wanted (the square bracket notation is actually shorthand for the list method ``__index__()``).

Ok, so that's an examlpe of how OOP is involved even when we're using "scripted" Python. But we can do better...  


### Modules

Even though we call `simple_script.py` a "script", any file that ends in `.py` and contains valid Python is technically a module. Often, modules are defined such that they can be imported into *other* code and used. (note: `simple_script.py` won't actually place nice if open a Python interpreter and `import simple_script` because it's waiting for something to engage `sys.stdin`). Instead, let's use the `simple_module.py` example. Open the file and have a look.

#### Part 1

In "part 1" of ``simple_module.py`` we define a couple of variables (at the outer-most level, this is one way people will create "global" variables in Python), and one function which returns the square of it's input. Start a CLI Python session (nb: if you use `ipython` you will have tab autocompletion and general merriment) from this project directory and import our module (optionally with an alias\*). Then prove to yourself that you can access the things in the top half of this module:

    In [1]: import simple_module as sm

    In [2]: sm.my_int
    Out[2]: 4

    In [3]: sm.square(6)
    Out[3]: 36


#### Part 2

In "part 2", we're starting to use some of the more rich OO structures. This part of the module defines a ``Dog`` class, which has two methods: ``__init__()`` ("dunder init"), and ``speak()``. ``__init__()`` is referred to as the constructor or the initializer, depending on what other languages one has learned; this is the method that gets called when you instantiate a new object of this particular class. The definition of the class often includes a base class from which we inherit things, and in Python 2.x, this is typically ``object`` (allows us to use newer features of Python). In Python 3, ``object`` doesn't have to be passed explicitly. More on inheritance later. 

When we create a new object based on a class, the constructor assigns that particular object all of the attributes defined in the constructor, and we can again address all the methods and variables (now called attributes):

    In [1]: import simple_module as sm

    In [2]: d1 = sm.Dog()       # create a Dog object

    In [3]: d1                  # without a __repr__(), we get the memory location 
    Out[3]: <simple_module.Dog at 0x10b1d0a10>

    In [4]: vars(d1)            # see all of the attributes of d1
    Out[4]: {'legs': 4, 'name': 'rex', 'owner': 'jane', 'word': 'woof'}

    In [5]: d1.legs             # access a particular attribute 
    Out[5]: 4

    In [6]: d1.speak()          # have d1 use its speak() method
    Out[6]: 'woof, my name is rex. i have 4 legs and belong to jane.'

    In [7]: d1.name = "lichtenstien"    # overwrite the name attribute in d1

    In [8]: d1.speak()          # note the different output 
    Out[8]: 'woof, my name is lichtenstien. i have 4 legs and belong to jane.'

    In [9]: d2 = sm.Dog()       # create another Dog

    In [10]: d2                 # note that this is a different memory location 
    Out[10]: <simple_module.Dog at 0x10b1d0cd0>

    In [11]: d2.speak()         # d2 has the same speak() method
    Out[11]: 'woof, my name is rex. i have 4 legs and belong to jane.'


Above, ``d1`` and ``d2`` are two unique instances of the same ``Dog`` class. As we've defined the ``Dog`` class, there's never going to be any variation from one ``Dog`` to another (at least upon creation - we could still reach in and overwrite the attributes). Sadness. But never fear, Part 3 brings hope...

#### Part 3

Finally, in "part 3", we have a ``Cat`` class definition similar to that of the ``Dog`` class, except note that the constructor takes arguments. There are a few ways to require or use arguments in the class definition for the creation of a new object. The first argument in any class constructor is ``self`` and this allows Python to use and access the attributes and methods that are unique to this particular instance. Later, when we want to manipulate or access these internal things, we can use the ``self.`` notation to do so. 

The first argument that we created is ``name`` and this is a required argument. If you try to create a ``Cat`` without passing in at least this one argument, you'll get a ``TypeError``. The second argument is ``legs``, but notice that in the constructor, we're already assigning it a default value. If you create a ``Cat`` and only give it a name, it will be created with four legs and an owner named John. However, since these arguments are in the constructor, you can override the default values. Importantly, the default arguments are positional, but if you pass them as keyword pairs the order doesn't matter. Some examples: 

    In [1]: import simple_module as sm

    In [2]: c = sm.Cat("fuzzball")

    In [3]: vars(c)
    Out[3]: {'legs': 4, 'name': 'fuzzball', 'owner': 'john', 'word': 'meow'}

    In [4]: c = sm.Cat("fuzzball", owner="josh", legs=56)       # as keywords, the argument order doesn't matter

    In [5]: c.speak()
    Out[5]: 'meow, my name is fuzzball. i have 56 legs and belong to josh.'

    In [6]: c = sm.Cat("garfield", "john", 4)                   # without keywords, arguments are positional

    In [7]: c.speak()
    Out[7]: 'meow, my name is garfield. i have john legs and belong to 4.'      # d'oh!


One final point on using a module like ``simple_module.py``. Whenever a module is imported, a bunch of magic happens behind the scenes. One such thing is that the attribute ``__name__`` gets assigned to whichever module imports the new one. If, however, the module is executed from the command line, the ``__name__`` attribute is assigned the value ``__main__``, which is why many modules have a test for this at the bottom. This is a way to show some default behavior, or a quick way to test the behavior of a module, but it isn't really adequate for a real test suite. Run ``simple_module.py`` from the command line to see an example, and check that the code at the bottom of the file that runs makes sense. 


#### Packages 

Often, there is a bunch of code (contained in many separate modules) that are logically related and should be carried around together. Think of the way ``gnacs`` contains many separate modules (``twacs.py``, ``fsqacs.py``, ...), contained within subdirectories of e.g. a Github repo. In a typical Python package, these directories will each have an __init__.py module with a single line in it that names all of the submodules (see, for example, the version in [``gnacs``](https://github.com/DrSkippy27/Gnacs/blob/master/acscsv/__init__.py)). The ``__init__.py`` is how Python knows that the files inside this directory are modules and that they can also be imported. Many of the commands that we use frequency (``gnacs.py``, all the Gnip code that Skippy has written, the "big" Python libraries like ``numpy``) are actually packages, because they contain a lot of code. It seems that the word "package" is the proper term, but "library" often gets used to mean the same thing. Packages are typically obtained through PyPI (via ``pip install ____``). 

Ideally, the naming of directories follows a logical hierarchy for the modules contained therein. In this repo, you'll find a directory called ``life`` which is perhaps haughty, but nonetheless representative of the submodules contained in it: ``beast.py`` and ``human.py``. These two modules represent different, specialized versions of ``life``. Open ``beast.py`` first and have a look. The ``Animal`` class definition and all of its methods should look familiar from the earlier examples. The new hotness comes when we create another class ``Dog``, which is derived from the more general ``Animal`` class. The first line of the constructor then allows us to use all of the ``Animal`` methods and attributes from a ``Dog``. Note that the ``Dog`` constructor also overrides a couple of the ``Animal`` attributes. 

If you stay at the bottom level of this project (the ``python-oop`` directory), you can still import the ``beast.py`` module because we've made ``life`` a package. Some example behavior:


    In [1]: from life import beast as b

    In [2]: a = b.Animal()

    In [3]: a.talk()
    Out[3]: " I'm None and hungry"

    In [4]: vars(a)
    Out[4]: {'hungry': True, 'name': None, 'speak': ''}

    In [5]: d = b.Dog("rex")

    In [6]: d.talk()
    Out[6]: "woof! I'm rex and hungry"

    In [7]: d.eat()

    In [8]: d.talk()
    Out[8]: "woof! I'm rex and not hungry"


The last section of this little walk-through combines many of the above concepts into the ``human.py`` module in the ``life`` package. Open that up and have a look. The most basic class is that of a ``Person`` where a few attributes are set to default, null-ish values. In fact, we don't need to assign any attributes here, but I wanted to include a base ``talk()`` method here that would include some default behavior. When you create a ``Woman`` object (which, note, has required arguments in addition to some keyword arguments) you get to override the boring defaults of the ``Person``, and you get a new method ``high_five()`` that isn't callable by a general ``Person`` object. 

Finally, in the last class definition in ``human.py``, the constructor has a combination of required arguments, default arguments that get passed to the parent constructor, and the keyword argument wildcard ``**kwargs``. This last one allows you to pass an arbitrarily-long list of ``key=value`` pairs to the constructor. After calling the parent constructor, you can see that we iterate through all of the key-value pairs, making an attribute of the former, and assigning it a value of the latter. Examples are always good. Here's a run-through of the different things that came from the ``life`` package: 


    In [1]: from life import *                      # since we know there's not much in life, * is ok
                                                    #   and gives access to beast and human modules
    In [2]: d = beast.Dog("fluffy")

    In [5]: w = human.Woman("sarah")                # requires a name

    In [6]: vars(w)
    Out[6]: {'eyes': 'blue', 'gender': 'female', 'name': 'sarah', 'word': 'yo'}

    In [7]: w.talk()
    Out[7]: 'yo, my name is sarah. my gender is female, and i have blue eyes.'

    In [8]: aw = human.AmericanWoman("jane")        # requires a name because Woman requires a name

    In [9]: vars(aw)
    Out[9]: {'eyes': 'brown', 'gender': 'female', 'name': 'jane', 'word': 'holla'}

    In [10]: aw.talk()                              # AmericanWoman has overwritten the talk() method

    Don't come hangin' 'round my door
    I don't wanna see your shadow no more.

    In [11]: aw.lenny_kravitz()
    Out[11]: 'guitar solo! ( http://www.youtube.com/watch?v=UzWHE32IxUc ) '

    In [12]: aw = human.AmericanWoman("jane", bear="teddy", cow=3)  # arb key-value pairs get assigned as attributes

    In [13]: vars(aw)
    Out[13]: 
    {'bear': 'teddy',
     'cow': 3,
     'eyes': 'brown',
     'gender': 'female',
     'name': 'jane',
     'word': 'holla'}


There is, of course, much more to say and know about all of these topics, so do look into the official docs for more information. 


fin. 

---------------------------------------------------------------
\*A note on import statements:
There are three common ways you'll see modules and packages imported; the differences are mainly in how much new stuff you add to the interpreter's namespace. That is, do you have to specifically reach through `sys` to get to `sys.stdin`, or do you have direct access to `stdin`? Examples of the three types of imports are as follows: 

    In [1]: import simple_module
    In [2]: simple_module.my_s
    Out[2]: 'hello world!'
    ####
    
    In [1]: import simple_module as sm      # same as above, but with alias
    In [2]: sm.my_int
    Out[2]: 4
    #### 

    In [1]: from simple_module import square
    In [2]: square(6)
    Out[2]: 36

    In [3]: my_int
    ---------------------------------------------------------------------------
    NameError                                 Traceback (most recent call last)
    <ipython-input-8-9b53895acf20> in <module>()
    ----> 1 my_int
    NameError: name 'my_int' is not defined
    ####

    In [1]: from simple_module import *
    In [2]: square(4)
    Out[2]: 16

    In [3]: my_s
    Out[3]: 'hello world!'


``import`` take-aways: 

- Python allows you to import all willy-nilly

- know that using ``import *`` is often considered "poor form"

- many package/module aliases have convention that would be good to follow (``mpl, plt, pd, np, sp, ...``)

- do whatever you want, but always assume the next person reading your code knows where you live


