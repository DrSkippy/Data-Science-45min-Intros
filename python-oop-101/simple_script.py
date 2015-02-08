#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="MIT License"

# import the sys module from the standard library (ie no need to pip install) 
import sys 

# data comes in via stdin, results are sent to stdout 
for cnt, line in enumerate(sys.stdin):
    body = line.split('|')[2]
    sys.stdout.write("line number: {}, tweet body: {}\n".format(cnt, body)) 
    # ^ this is ~equivalent to "print(stuff)"
