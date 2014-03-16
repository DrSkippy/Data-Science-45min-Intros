#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="MIT License"

import unittest

class Test_Foo(unittest.TestCase):
    """
    Test module to go along with test discovery example 
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_baz(self):
        self.assertEqual(0,0)

    def test_bar(self):
        self.assertIsInstance("josh", str)


if __name__ == '__main__':
    unittest.main()

