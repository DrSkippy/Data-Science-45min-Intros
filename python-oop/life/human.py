#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="MIT License"


class Person(object):
    """Create a general Person object."""
    def __init__(self):
        self.gender = None 
        self.name = None 
        self.eyes = None 
        self.word = "uhnnnnn" 

    def talk(self):                   
        """Use the Person's specific attributes to 'talk'."""
        s = "{}, my name is {}. my gender is {}, and i have {} eyes.".format(
                self.word
                , self.name
                , self.gender
                , self.eyes
                )
        return s

class Woman(Person):
    """
    Create a Woman object, derived from a Person object. Requires a name, and 
        takes optional keyword arguments 'eyes' (color), and 'word'.
    """
    def __init__(self, name, eyes="blue", word="yo"):
        super(Woman, self).__init__()       # inherit attrs & methods from Person 
        self.name = name                    # overwrite attrs for these objects 
        self.eyes = eyes 
        self.word = word 
        self.gender = "female"              # set this one attr

    def high_five(self):
        """Return a badass high-five."""
        return "High-five!"
    

class AmericanWoman(Woman):
    """Create an American Woman object, derived from a Woman object."""
    def __init__(self, name, eyes="brown", word="holla", **kwargs):
        super(AmericanWoman, self).__init__(name, eyes, word)
        [ setattr(self, k, v) for k,v in kwargs.iteritems() ]

    def talk(self):
        """Override the talk method in the Person class"""
        s = "\nDon't come hangin' 'round my door\nI don't wanna see your shadow no more."
        print s

    def lenny_kravitz(self):
        """Make Lenny Kravitz proud.""" 
        return "guitar solo! ( http://www.youtube.com/watch?v=UzWHE32IxUc ) "



