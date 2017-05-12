#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#   Scott Hendrickson
#     2011-09-15

import codecs
import sys

#reload(sys)
#sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
#sys.stdin = codecs.getreader('utf-8')(sys.stdin)

class SS2Similar(object):

    def __init__(self, _maxOffset):
        self.maxOffset = _maxOffset
    
    # s1 and s2 are lists of words in order
    def distance(self, s1, s2):
        if s1 is None or len(s1) < 1:
            if s2 is None or len(s2) < 1:
                return 0.
            else:
                return len(s2)
        if s2 is None or len(s2) < 1:
            return len(s1)
        c = 0
        offset1 = 0
        offset2 = 0
        dist = 0
        while c + offset1 < len(s1) and c + offset2 < len(s2):
            if s1[c + offset1] != s2[c + offset2]:
                offset1 = 0
                offset2 = 0
                for i in range(0, self.maxOffset):
                    if c + i < len(s1) and s1[c + i] == s2[c]:
                        if i > 0:
                            dist += 1
                            offset1 = i
                            break   
                    if c + i < len(s2) and s1[c] == s2[c + i]:
                        if i > 0:
                            dist += 1
                            offset2 = i
                        break
                else:
                    dist += 1
            c += 1
        return dist + (len(s1) - offset1 + len(s2) - offset2)/2. - c
    
    def similarity(self, s1, s2):
        dis = self.distance(s1, s2);
        maxLen = max(len(s1), len(s2))
        if maxLen == 0:
            return 1.
        else:
            return 1. - dis / maxLen



if __name__ == '__main__':
    import re
    # this set is classified fairly well at shift:30 and score > 0.5
    strings = [ 
     "On the topic of Strata Talk. If you live in a stratified building, this website might be of interest to you. http://t.co/SWEUxBCP"
    ,                             "If you live in a stratified building, this website might be of interest to you. http://t.co/SWEUxBCP"
    ,"On the topic of Strata Talk. If you live in a stratified building, this website"
    ,                                    "live in a stratified building, this website might be of interest"
    ,"Happy birthday to you now. On the topic of Strata Talk. If you live in a stratified building, this website might be of interest to you. http://t.co/SWEUxBCP"
    ,"On the topic of Strata Talk. If you live in a stratified building, this website might be of interest to you. http://t.co/SWEUxBCP Happy birthday to you now."
    ,"On tsdfadhe topic of Stasdfadsrata Talk. Ifasdf you live in a stratifdfgsdsded building, this website might be of interest to you. http://t.co/SWEUxBCP"
    ,"On tsdfadhe topic of Stasdfadsrata Talk. Ifasdf you live in a stratifdfgsdsded buisdfasdlding, this weasdfasdbfsite might be oasdffasdfasdt.co/SWEUxBCP"
    ,"Social media index for businesses and industries. Also, a couple of good info design ideas bit.ly/r5tfqg"
    ,"lk. If you live in a stratified building, this website might be of interest to you. http://t.co/SWEUxBCP"
    ]
    for shift in range(1,15):
        ss = SS2Similar(shift)
        for i in range(0,len(strings)):
            for j in range(i,len(strings)):
                print(i,j,shift, ss.similarity(re.split('\W+', strings[i]), re.split('\W+', strings[j])))
                print(strings[i])
                print(strings[j])
