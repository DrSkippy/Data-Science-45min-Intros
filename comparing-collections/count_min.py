#!/usr/bin/env python
# encoding: utf-8

"""
cmsketch.py

An implementation of count-min sketching from the paper due to Cormode and
Muthukrishnan 2005

"""

import sys
import random
import numpy as np
import heapq
import json
import time
import operator
import collections

BIG_PRIME = 9223372036854775783

def random_parameter():
    return random.randrange(0, BIG_PRIME - 1)

# Count Min sketch helper functions for Enumerator

def cms_combiner(current_cms_obj, new_value):
    if isinstance(new_value,Sketch):
        current_cms_obj.combine(new_value)
    else:
        current_cms_obj.update(new_value, 1)
    return current_cms_obj
def cms_evaluator(sketch):
    top_n = list(
                reversed(
                    sorted(sketch.top_k.values(), key=operator.itemgetter(0))
                )
            )
    output_list = []
    counter = 1
    for item in top_n:
        output_list.append({"key":"item {0:d}".format(counter),"value":item[1]})
        output_list.append({"key":"count {0:d}".format(counter),"value":int(item[0])})
        counter += 1
    return output_list
        

class Sketch:
    def __init__(self, kwargs):
        """
        Setup a new count-min sketch with parameters delta, epsilon and k

        The parameters delta and epsilon control the accuracy of the
        estimates of the sketch

        Cormode and Muthukrishnan prove that for an item i with count a_i, the
        estimate from the sketch a_i_hat will satisfy the relation

        a_hat_i <= a_i + epsilon * ||a||_1

        with probability at least 1 - delta, where a is the the vector of all
        all counts and ||x||_1 is the L1 norm of a vector x

        Parameters
        ----------
        delta : float
            A value in the unit interval that sets the precision of the sketch
        epsilon : float
            A value in the unit interval that sets the precision of the sketch
        k : int
            A positive integer that sets the number of top items counted

        Examples
        --------
        >>> s = Sketch(10**-7, 0.005, 40)

        Raises
        ------
        ValueError
            If delta or epsilon are not in the unit interval, or if k is
            not a positive integer

        """

        delta = kwargs['delta']
        epsilon = kwargs['epsilon']
        k = kwargs['k']

        if delta <= 0 or delta >= 1:
            raise ValueError("delta must be between 0 and 1, exclusive")
        if epsilon <= 0 or epsilon >= 1:
            raise ValueError("epsilon must be between 0 and 1, exclusive")
        if k < 1:
            raise ValueError("k must be a positive integer")

        self.w = int(np.ceil(np.exp(1) / epsilon))
        self.d = int(np.ceil(np.log(1 / delta)))
        self.k = k
        self.hash_functions = [self.__generate_hash_function() for i in range(self.d)]
        self.count = np.zeros((self.d, self.w), dtype='int32')
        self.heap, self.top_k = [], {} # top_k => key, [estimate, key] pairs

    def update(self, key, increment):
        """
        Updates the sketch for the item with name of key by the amount
        specified in increment

        Parameters
        ----------
        key : string
            The item to update the value of in the sketch
        increment : integer
            The amount to update the sketch by for the given key

        Examples
        --------
        >>> s = Sketch(10**-7, 0.005, 40)
        >>> s.update('http://www.cnn.com/', 1)

        """
        for row, hash_function in enumerate(self.hash_functions):
            column = hash_function(abs(hash(key)))
            self.count[row, column] += increment

        self.update_heap(key)

    def update_heap(self, key):
        """
        Updates the class's heap that keeps track of the top k items for a
        given key

        For the given key, it checks whether the key is present in the heap,
        updating accordingly if so, and adding it to the heap if it is
        absent

        Parameters
        ----------
        key : string
            The item to check against the heap

        """
        estimate = self.get(key)

        if not self.heap or estimate >= self.heap[0][0]:
            if key in self.top_k:
                #update top_k
                old_pair = self.top_k.get(key)
                old_pair[0] = estimate
                #update heap queue
                for item in self.heap:
                    if item[1] == key:
                        item[0] = estimate
                heapq.heapify(self.heap)
            else:
                if len(self.top_k) < self.k:
                    heapq.heappush(self.heap, [estimate, key])
                    self.top_k[key] = [estimate, key]
                else:
                    new_pair = [estimate, key]
                    old_pair = heapq.heappushpop(self.heap, new_pair)
                    if new_pair[1] != old_pair[1]:
                        del self.top_k[old_pair[1]]
                        self.top_k[key] = new_pair

    def get(self, key):
        """
        Fetches the sketch estimate for the given key

        Parameters
        ----------
        key : string
            The item to produce an estimate for

        Returns
        -------
        estimate : int
            The best estimate of the count for the given key based on the
            sketch

        Examples
        --------
        >>> s = Sketch(10**-7, 0.005, 40)
        >>> s.update('http://www.cnn.com/', 1)
        >>> s.get('http://www.cnn.com/')
        1

        """
        value = sys.maxsize
        for row, hash_function in enumerate(self.hash_functions):
            column = hash_function(abs(hash(key)))
            value = min(self.count[row, column], value)

        return value

    def combine(self, new_sketch):
        """
        Combines a new sketch with the current sketch. 
        Sketch combination is exact; new top_k list is approximate.

        Must combine counting array and top_k list.
        """
        self.count += new_sketch.count

        counts_dict = collections.defaultdict(int)
        
        # top_n dictionary entries have the form:
        #    key : (value, key)
        #
        for v,k in self.top_k.values() + new_sketch.top_k.values():
            counts_dict[k] += v
        
        sorted_kv_pairs = list(reversed(sorted(counts_dict.items(),key=operator.itemgetter(1))))
        top_kv_pairs = sorted_kv_pairs[0:self.k]
        self.top_k = {}
        for key, value in top_kv_pairs:
            self.top_k[key] = [value, key]

    def __generate_hash_function(self):
        """
        Returns a hash function from a family of pairwise-independent hash
        functions

        """
        a, b = random_parameter(), random_parameter()
        return lambda x: (a * x + b) % BIG_PRIME % self.w

if __name__ == '__main__':
    def print_results(s):
        print('Top tweeters')
        for value in s.top_k.values():
            print('{0} {1}'.format(str(value[0]),str(value[1])))
        print('\n')

    s = Sketch(dict(delta=10**-5,epsilon=0.001,k=20))
    now = time.time()
    for line in sys.stdin:
        if time.time() - 5 > now:
            now = time.time()
            #print_results(s)
        try:
            user_name = json.loads(line)['actor']['preferredUsername']
        except ValueError:
            continue
        except (KeyError, e):
            continue
        
        s.update(user_name,1)
    
    print_results(s)

