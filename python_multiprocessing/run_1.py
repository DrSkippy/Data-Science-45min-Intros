#!/usr/bin/env python

import time

def bad_ass_function(n):
    t = time.time
    u = t() + n
    while t() < u:
        pass
    return "finished {}s of badass-ery".format(n)

## start by calling a function

if __name__ == "__main__":
    n = 3
    ret_val = bad_ass_function(n)
    print(ret_val)

"""
To parallelize, we much first run a process in a different thread
"""
