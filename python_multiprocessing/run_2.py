#!/usr/bin/env python

from multiprocessing import Process
from run_1 import bad_ass_function

if __name__ == "__main__":
    n = 5
    # Process takes keyword args: target=function_name, args=function_args_tuple
    p = Process(target=bad_ass_function,args=(n,))
    
    # runs "target" locally
    #p.run()
    
    # calls "p.run" in a new thread
    #p.start()
    
    # block this thread until p terminates
    #p.join()
    
    print("finished first process")

    #q = Process(target=bad_ass_function,args=(n,))
    #q.start()
    
    
"""
But what about the return value of the function?
"""
    
