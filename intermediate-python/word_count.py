from mrjob.job import MRJob
import re


WORD_RE = re.compile(r"[\w']+")

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        for word in WORD_RE.findall(line):
            yield word.lower(), 1

    def combiner(self, word, counts):
        yield word, sum(counts)

    def reducer(self, word, counts):
        yield word, sum(counts)

#    # another example from the mrjob docs
#    def mapper(self, _, line):
#        # here's one version of an MR counter: summary stats
#        yield "chars", len(line)
#        yield "words", len(line.split())
#        yield "lines", 1
#
#    def reducer(self, key, values):
#        yield key, sum(values)

if __name__ == '__main__':
    MRWordFrequencyCount.run()
