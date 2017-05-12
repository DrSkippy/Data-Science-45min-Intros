#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
from similarity_words import *
import sys
import codecs
import re
import argparse

#reload(sys)
#sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
#sys.stdin = codecs.getreader('utf-8')(sys.stdin)

class duplicateFilter(object):

    def __init__(self, threshold = 0.65):
            self.thresh = threshold
            self.retweetedMemory = []
            self.recentTweetMemory = []
            self.retweetedMemorySize = 15
            self.recentTweetMemorySize = 3000
            self.ss = SS2Similar(5)
            #
            self.logf = open('./removeDups.log','w')
            self.logf.write("*"*42 + "\n")
            #
            self.hist = {}
            for i in range(int(threshold*100),101):
                    self.hist[i] = 0
            self.countRepeats = 0
            self.countMatches = 0
            self.countShort = 0

    def isDup(self, id, text):
            result = True
            tweetList = [x for x in re.split('\W+', text) if x != '']
            newPair = [id, tweetList]
            if len(newPair[1]) > 2:
                    # check the memory of recent tweets first
                    for pair in self.recentTweetMemory:
                            score = self.ss.similarity(newPair[1], pair[1])
                            if score > self.thresh:
                                    self.countRepeats += 1
                                    break # one match is all we need
                    else: # only do this if we finished the above loop without a match
                            # check agaist unique tweet memory
                            for pair in self.retweetedMemory:
                                    score = self.ss.similarity(newPair[1], pair[1])
                                    if score > self.thresh:
                                            self.recentTweetMemory.append(pair)
                                            self.hist[int(score*100)] += 1
                                            self.countMatches += 1
                                            break # one match is all we need
                            else: # only do this if we finish without a match!
                                    result = False
                    self.retweetedMemory.append(newPair)
                    if len(self.retweetedMemory) > self.retweetedMemorySize:
                            self.retweetedMemory.pop(0)
            else:
                    self.countShort += 1
            if len(self.recentTweetMemory) > self.recentTweetMemorySize:
                    self.logf.write(str(self.recentTweetMemory.pop(0)) + '\n')
            return result

    def writeRetweetsToLog(self):
            self.logf.write("Retweet memory dump at end of run (size smaller of (%d,%d)):\n"%(self.countMatches, self.recentTweetMemorySize))
            for a in self.recentTweetMemory:
                    self.logf.write("%s\n"%str(a))
    
    def writeHistToLog(self):
            self.logf.write("*"*42 + "\n")
            for a in self.hist:
                    self.logf.write("%d, %s\n"%(a, self.hist[a]))
            self.logf.write("\n**************\nHit rates:\n")
            self.logf.write(" Original matches: %d\n"%self.countMatches)
            self.logf.write(" Repeat matches: %d\n"%self.countRepeats)
            self.logf.write(" Short tweets: %d\n"%self.countShort)
            self.logf.write(" Total repeated (filtered) Tweets: %d\n"%(
                self.countShort+self.countRepeats+self.countMatches))

if __name__ == '__main__':

    def args():
        args_parser = argparse.ArgumentParser(
                description="Command line duplicate and near match filtering")
        args_parser.add_argument("-c", "--column", dest="col_txt",
                default=2, help="Column containing the text to deplup on [default is 2nd column]")
        args_parser.add_argument("-i", "--index-column", dest="col_idx",
                default=1, help="Column containing the unique identifier for the item [default is 1st column]")
        args_parser.add_argument("-d", "--delimiter", dest="delimiter", 
                default="|", 
                help="Delimiter. Default is pipe |")
        args_parser.add_argument("-l", "--logging", dest="log_flag", action="store_true", 
                default=False, help="Log discarded duplicates")
        args_parser.add_argument("-t", "--threshold", dest="command_line_threshold", default=65)
        return args_parser
    
    options = args().parse_args()
    id_txt = int(options.col_txt)-1
    id_idx = int(options.col_idx)-1
    t = int(options.command_line_threshold)*.01
    f = duplicateFilter(t)
    for row in sys.stdin:
        row = row.strip().split(options.delimiter)
        if not f.isDup(row[id_idx],row[id_txt]):
            print(options.delimiter.join(row))
        # else do something with dups here
    f.writeRetweetsToLog()
    if options.log_flag:
        f.writeHistToLog()
