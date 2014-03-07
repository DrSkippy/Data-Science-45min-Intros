# Testing Code in Python with ``unittest``
2014-03-07, RST

Python's ``unittest`` framwork is modeled after ``jUnit`` (java), which is an implementation of the general ``xUnit`` framework for unit testing. 

features:

- automation
 
- setup & teardown

- aggregation of tests

## Concepts

#### test fixture

preparation for one or more tests, e.g. temporary databases, directories, servers


#### test case

smallest unit of testing; specific response to a specific set of inputs 

#### test suite

collection of test cases, suites, or both. can be used to aggregate tests that are logically related

#### test runner

organizes the execution of tests (ie through GUI or CLI)


Instances of the ``TestCase`` class are the smallest testable units. Implements the interface required by the test runner and the methods that the test code can use to check and report results to the user. Project- and code-specific test classes can (should) inheriti from ``TestCase``. A new ``TestCase`` is created for each test method. 

We won't dive into the full depths of ``unittest``, but rather see it in action in a simple case, write some tests, then see a bigger version, in use. 

----

## Code Example

Defined here is a module called ``mathy.py`` (nb: ``math`` is a real thing, so avoid clobbering it in the namespace). It has some very simple functionality, demonstrated below:

    $ ipython
    In [1]: import mathy as m

    In [2]: c = m.Calcs()       # create a calculations object

    In [3]: c.zero              # return an instance attribute 
    Out[3]: 0

    In [4]: c.square(4)         # use the instance methods 
    Out[4]: 16

    In [5]: c.add_one(84.2)
    Out[5]: 85.2

Open up the code and have a look. There are a couple of methods and an example of a simple error handling case (try block) in one method to avoid having the code crash in a fiery death. In a production environment, you'd probably be sad if your entire application failed because some smarty-pants passed a string to your numerical calculation. The other method is left as an example for testing.


## Test Example

Now that we have some code, we can build a test suite to make sure that it still behaves the way we want with every new feature or modification. Ideally, you develop the test code in parallel with your actual application; it may often be easier to express how you'd *like* the code to run than to actually get it to run that way.

First, just run the ``test_mathy.py`` module from the command line so you can see what the output looks like. Ideally, it will say that all the tests have passed and also tell you how many it ran. Now have a look at the code in the test module. 

The first thing we have to do is import the module we're testing, in this case the ``mathy`` module. Then you can import any other modules that will help / be needed. Additionally, you have to import the actual ``unittest`` module. Next, we define a test class that will test all the moving parts of the particular module in which we're interested. There could be many classes defined in ``mathy``, and but we can (and will) test them all in the ``test_mathy`` test suite. The test class needs to inherit from the ``TestCase`` module and this allows us to use all of the ``assert____`` methods seen in the rest of the code. For a list of all the possible methods, check [the documentation](http://docs.python.org/2/library/unittest.html). 


Each test method defined in the class will run independently, and the ``setUp`` and ``tearDown`` methods will run, respectively before and after each of the test methods. This ensures the tests have consistency (or randomness if you design it that way e.g. with the ``random`` module). In this ``setUp`` method, we're creating a handful of test arguments. Each ``test_*`` method is independent of the others, so as soon as one of the tests (``self.assert...``) fails, that method stops evaluating and the test runner moves to another test. *Importantly*, the tests do not necessarily execute in the order they are listed. This is part of the value of (and need for) the ``setUp`` and ``tearDown`` methods.

Finally, if you have a full package (ie our last RST) which includes many modules and many test suites, you can run them all by using the built-in command line test discovery. From the top-level directory in your project, run:

``$ python -m unittest discover``

There are options associated with ``discover`` that allow you to specify the naming convention of your test code, but the default is to execute any and all modules that look like ``test*.py``. If you run the discover statement above, you'll now see that more tests have been run, because ``discover`` has also run the two (trivial) tests found in ``test_foo.py``


## Your turn

Add some new functionality to the ``mathy`` class: an attribute, a new method, whatever you like, but only add one thing. Then start writing the test code for the feature you've added; you should think hard about *all* the various ways you can test that the rest of the code is interacting as you expected. Boolean logic, checking for type, None-ness, equality... The real wins from using ``unittest`` come from knowing that you can always re-run your test suite after each edit to the code to ensure all the smallest pieces are still working as expected. Your test code should grow much faster than your running code. And if you find yourself adding a feature for which there isn't a good test, consider whether you can reframe the purpose and implementation of the code into a deterministic, test-able form. 

## A larger example of application testing

...





