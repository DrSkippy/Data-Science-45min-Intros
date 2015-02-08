#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="MIT License"


class Calcs(object):
    """
    Objects of type Calcs have two methods for numerical calculations, and 
    an attribute of 'zero' which is set to 0
    """

    def __init__(self):
        self.zero = 0

    def add_one(self, x):
        """Return the argument incremented by 1"""
        try:
            return x + 1
        except TypeError:   # be gentle
            return "And what, exactly would it mean to add one to {}?".format(x)

    def square(self, x):
        """Return the square of the argument""" 
        return x**2     # no exception handling
 
