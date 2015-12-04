#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
A simple module representing a Coordinate class and related method. 

Modified from Simeon Franklin's blog:
- http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/ 
"""

class Coordinate(object):
    """Represents a point in two-dimensional space."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Coord: " + str(self.__dict__)

def add(a, b):
    """Combine two Coordinates by addition."""
    return Coordinate(a.x + b.x, a.y + b.y)

