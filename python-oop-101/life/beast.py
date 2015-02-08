#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="MIT License"


class Animal(object):
    """Create a generic Animal object."""
    def __init__(self):         # generic Animal takes no arguments
        self.hungry = True      # born hungry 
        self.name = None
        self.speak = ""

    def eat(self):
        """Set hungry attribute to False"""
        self.hungry = False

    def run(self):
        """Set hungry attibute to True."""
        self.hungry = True

    def talk(self):
        """Return the 'vocal' representation of this object."""
        hunger = "hungry" if self.hungry else "not hungry"
        return "{} I'm {} and {}".format(self.speak, self.name, hunger) 

class Dog(Animal):
    """Create a Dog object, inherits from Animal object"""
    def __init__(self, name):   # at the risk of anthropomorphizing, a dog must have a name 
        super(Dog, self).__init__()
        #nb: in this case, the use of "super" is ~ as saying "Animal.__init__()"
        #       but for multiple inheritance, becomes more obviously valuable 
        self.name = name
        self.speak = "woof!"    # dogs should woof by default 

        
