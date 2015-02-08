#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="MIT License"

import sys


######################
# part 1
#

my_int = 4 
my_s = "hello world!"

def square(number):
    """Return the squared value of 'number'."""
    try:
        return number**2
    except TypeError as e:
        sys.stderr.write("Can't square something that's not a number! ({})".format(e))


######################
# part 2
#

class Dog(object):
    """Create a general Dog object. Takes no arguments."""
    def __init__(self):
        self.name = "rex"
        self.legs = 4
        self.owner = "jane"
        self.word = "woof"
        
    def talk(self):
        """Return a statement about the attributes of this Dog."""
        s = "{}, my name is {}. i have {} legs and belong to {}.".format(
                self.word
                , self.name
                , self.legs
                , self.owner
                )
        return s


######################
# part 3
#

class Cat(object):
    """
    Create a general Cat object. Requires a name and optional count of legs
    and owner name.
    """
    def __init__(self, name, legs=4, owner="john"):
        self.name = name
        self.legs = legs        # note that we're not doing any type checking... 
        self.owner = owner 
        self.word = "meow"
        
    def talk(self):
        """Return a statement about the attributes of this Dog."""
        s = "{}, my name is {}. i have {} legs and belong to {}.".format(
                self.word
                , self.name
                , self.legs
                , self.owner
                )
        return s



##################################################
if __name__ == '__main__':
    print   # cheap carriage returns in stdout
    sys.stdout.write("Now creating a Cat named Sue, with 84 legs, belonging to Jeff.")
    sys.stdout.write(".\n"*10)
    c = Cat("Sue", legs=84, owner="jeff")
    sys.stdout.write("SPEAK, CAT!")
    print
    print
    sys.stdout.write('"' + c.talk() + '"')
    print
    print
