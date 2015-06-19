#!/usr/bin/env python

from multiprocessing import Process, Pool, Queue
import time
import sys

def bad_ass_function(n):

    t = time.time
    u = t() + n
    while t() < u:
        pass
    return_str = "finished {}s of badass-ery".format(n)
    return return_str

if __name__ == "__main__":
    
    queue = Queue()
    pool = Pool()
    n = 3    

    ## in analogy with "apply"
    #print(pool.map(bad_ass_function,[n,6,8,9]))

    ## ...and with apply_async
    result = pool.map_async(bad_ass_function,[n,6,8,9])
   
    ### WEIRDNESS: if "result" is not queried with "ready" function, processes do not run
    
    while not result.ready():
        print("waiting 2 seconds")
        time.sleep(2)
    print(result.get())


"""
 NOTES:

    "map" and "apply" (along with "filter") should remind you 
of scala, and are some of the fundamental building blocks of 
functional programming. Get used to thinking in terms of them.

"""
