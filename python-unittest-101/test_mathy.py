#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="MIT License"

import mathy 
import random
import string
import unittest


class Test_mathy(unittest.TestCase):
    """
    Test module for the practice mathy.py module
    """

    def setUp(self):
        """
        Create an instance of the Calcs class for use with all test methods 
        """
        # assign some instance vars so we can use them in subsequent tests
        #   in lieu of global vars
        self.f = random.normalvariate(0, 1)         # random float
        self.i = int( random.uniform(0, 10) )       # random int 
        self.s = random.choice( [x for x in string.lowercase] )  # random string char 
        # create a new object of type Calcs for testing
        self.calcs = mathy.Calcs()                  # use this object for the tests 
        
    def tearDown(self):
        """ 
        Clean up anything e.g. database connections that needs to be taken care of 
        after each test
        """
        pass

    def test_init(self):
        """
        Test that the constructor is behaving as expected
        """
        self.assertIsInstance(self.calcs, mathy.Calcs)
        self.assertIsInstance(self.calcs.zero, int)
        self.assertEqual(self.calcs.zero, 0)

    def test_add_one(self):
        """
        Test that the add_one method is behaving as expected 
        """
        # floats and ints should be happy
        # check the value
        self.assertEqual(self.calcs.add_one(self.f), self.f + 1)
        self.assertEqual(self.calcs.add_one(self.i), self.i + 1)
        # check the type
        self.assertIsInstance(self.calcs.add_one(self.i), int)
        self.assertIsInstance(self.calcs.add_one(self.f), float)
        # check the exception 
        self.assertIsInstance(self.calcs.add_one(self.s), str)

    def test_square(self):
        """
        Test that the square method is behaving as expected 
        """
        # check the values
        self.assertEqual(self.calcs.square(self.f), self.f**2)
        self.assertEqual(self.calcs.square(self.i), self.i**2)
        # check the type
        self.assertIsInstance(self.calcs.square(self.f), float)
        self.assertIsInstance(self.calcs.square(self.i), int)
        # check the exception
        #
        # because of the way the expression is evaluated, 
        #   there are two ways to check the exception handling...
        # ==>   lambda fnc
        self.assertRaises(TypeError, lambda: self.calcs.square(self.s))
        # ==>   contextmanager
        with self.assertRaises(TypeError):
            self.calcs.square(self.s)


if __name__ == '__main__':
    unittest.main()

