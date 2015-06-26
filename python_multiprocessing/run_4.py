#!/usr/bin/env python

from multiprocessing import Process, Pool, Queue
import time
import sys

def bad_ass_function(**kwargs):
    n = int(kwargs["n"])

    t = time.time
    u = t() + n
    while t() < u:
        pass
    return_str = "finished {}s of badass-ery".format(n)
    if "queue" in kwargs:
        kwargs["queue"].put(return_str)
    else:
        return return_str

def dump_results_list(results_list):
    ## iterate over results until they're all done 
    output = []
    while len(results_list) > 0:
        print("{} processes still running".format(len(results_list)))
        for result in results_list:
            if result.ready():
                output.append(result.get())
                results_list[:] = [ r for r in results_list if r!=result ]
        time.sleep(2)

    ## print the results
    [ sys.stdout.write(str(o)+"\n") for o in output ]

if __name__ == "__main__":
    
    queue = Queue()
    pool = Pool()
    n = 3    

    ## "apply" takes positional args: function_name, function args tuple, function kwargs dict 
    ##e us "apply" in analogy with Process objects
    #pool.apply(bad_ass_function,None,{"queue":queue,"n":n})
    
    ## whoops...Pool objects don't like queues
    #pool.apply(bad_ass_function,tuple(),{"n":n})
    
    ## Pool objects have a more familiar return strategy
    #return_val = pool.apply(bad_ass_function,tuple(),{"n":n})
    #print(return_val)

    ## now parallelize
    #for n in range(4):
    #    return_val = pool.apply(bad_ass_function,tuple(),{"n":n})
    #    ##print(type(return_val))
    #    print(return_val)
           
    ## "apply" is not asynchronous; use "apply_async, which returns a special results object"
    #results_list = [] 
    #for n in [4,5,9,10]:
    #    results_list.append( pool.apply_async(bad_ass_function,tuple(),{"n":n}) )
    #
    #dump_results_list(results_list)
