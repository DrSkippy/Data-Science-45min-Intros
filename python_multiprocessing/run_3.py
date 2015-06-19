#!/usr/bin/env python

from multiprocessing import Process, Queue
import time

def bad_ass_function(**kwargs):
    n = int(kwargs["n"])
    q = kwargs["queue"]    

    t = time.time
    u = t() + n
    while t() < u:
        pass
    return_str = "finished {}s of badass-ery".format(n)
    q.put(return_str)

def dump_queue(q):
    print("emptying queue:")
    while not q.empty():
        print(q.get())
    print("queue is empty")

if __name__ == "__main__":
    n = 3
    queue = Queue()
    # Process takes keyword args: target=function_name, args=function_args_tuple, kwargs=function_kwargs_dict
    p1 = Process(target=bad_ass_function,kwargs={"n":n,"queue":queue})
    
    # calls "p.run" in a new thread
    #p1.start()
    
    # block this thread until p1 terminates
    #p1.join()
   
    # create two new Process objects 
    #n = 5
    #p2 = Process(target=bad_ass_function,kwargs={"n":n,"queue":queue})
    #time.sleep(1)
    #p3 = Process(target=bad_ass_function,kwargs={"n":n,"queue":queue})

    #p2.start()
    #p3.start()
    #dump_queue(queue)
    
    #p3.join()
    #dump_queue(queue)
    

    
