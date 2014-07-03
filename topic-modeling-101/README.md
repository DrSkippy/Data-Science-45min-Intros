#Topic Modeling

Finding a thread of similarity between a set of texts.

##Definitions:
* 1.) document - a body of text (eg. tweet)
* 2.) text corpus - the set of documents that contains the text for the analysis (eg. many tweets)
* 3.) dictionary - a mapping between tokens and their integer ids. In other words, the key:value pairs are token:unique_id for each unique token in the text corpus (eg. {'mathematics':1,'engineering':1,'physics':3})
* 4.) vector corpus - the set of documents transformed such that each token is a tuple (token_id , doc_freq).


##Stop words:
**Topics are limited to tokens contained within the text corpus**. We can remove specific tokens from consideration using a set of stopwords, which can be edited per project requirement. 

<pre>
from nltk.corpus import stopwords
import pprint as pp

stopset = set(stopwords.words('english'))
print type(stopset)
stopset.update(["ruby tuesday"]) # add token
stopset.remove("own")            # remove token

# single lang
print "--English stopset"
print stopset

# multi lang
print
print "--Multi language stopset"
langs=['danish', 'dutch', 'english', 'french', 'german', 'italian','norwegian', 'portuguese', 'russian', 'spanish', 'swedish']
stop_list = []
for lang in langs:
    stop_list.extend(stopwords.words(lang))

stop_words_set=set(stop_list) #  -- could save to disk --
print stop_words_set
</pre>

##Text Corpus:
The text corpus used for the demo is contained in a file with lines of text separated by carriage returns. Each line of text is it's own document. We will use the entire text corpus as our training set to build the dictionary and then remove stopwords; however, the dictionary need not be built from the entire text corpus if a smaller set of documents is sufficient. 

<pre>
with open('text_corpus.txt', 'r') as f:
    documents=[]
    for line in f.readlines():
        documents.append(line.strip())
pp.pprint(documents)    
</pre>

##Dictionary:
Next, we'll create a dictionary from the tokens in the entire text corpus. We're splitting the documents on white space for this demo; however, we'll use regex in later. We'll then remove stopwords and tokens that only appear once in the entire text corpus.

<pre>

from gensim import corpora, models, similarities
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO, filename="./log/topic-log")
logr = logging.getLogger("topic_model")
logr.info("#"*15 + " started " + "#"*15)

print "Dictionary (full text corpus):"
dictionary = corpora.Dictionary(line.lower().split() for line in open('text_corpus.txt'))
print dictionary
print (dictionary.token2id)

print

print "Dictionary (removed stopwords and once-ids):"
stop_ids = [dictionary.token2id[stopword] for stopword in stop_words_set if stopword in dictionary.token2id]

once_ids = [tokenid for tokenid, corpus_freq in dictionary.dfs.iteritems() if corpus_freq == 1]
#remove stop_ids,"+",once_ids
dictionary.filter_tokens(bad_ids=stop_ids + once_ids,good_ids=None)
## consider: dictionary.filter_extremes(no_below=2) 
dictionary.compactify()
print dictionary
print (dictionary.token2id)
</pre>

We can also **add documents dynamically**, which is a huge advantage for real time data! Notice how the dictionary starts with 12 unique tokens (above) and ends with 25 tokens (below). Also note that we must add a list of lists such that docs=[[doc1],[doc2]...] where doc1 and doc2 are tokenized strings. 

<pre>
import copy
print "Add documents to dictionary dynamically:"
print "doc to add = \"Pooh bear says, 'People say nothing is impossible, but I do nothing every day.'\""
print
print "doc tokenized =",[item for item in "Pooh bear says 'People say nothing is impossible, but I do nothing every day.'".lower().split() if item not in stop_ids]
print

docs=[[item for item in "Pooh bear says, 'People say nothing is impossible, but I do nothing every day.'".lower().split() if item not in stop_ids]]
d=copy.deepcopy(dictionary)
d.add_documents(docs)

d.compactify()

print "#NOTE: since we were only splitting on space, the punctuation is included."
print
print d
print d.token2id
</pre>

##Vectorize:
Essentially a word frequency for each document is created in this step. Each document in the text corpus will be transformed into list of tuples 
[[(token_id , doc_freq),(token_id , doc_freq),(token_id , doc_freq)] , [(token_id , doc_freq),(token_id , doc_freq)]...]. We must iterate through the text corpus to create this set.

<pre>
vector_corpus=[]
with open('text_corpus.txt', 'r') as f:
    for line in f.readlines():
        vector_corpus.append(dictionary.doc2bow(line.lower().split()))

print "Vector corpus:"
pp.pprint(vector_corpus)
counter=0
print dictionary

# save to disk
corpora.MmCorpus.serialize('vector_corpus.mm', vector_corpus)
serialized_corpus = corpora.MmCorpus('vector_corpus.mm')
pp.pprint(list(serialized_corpus))
</pre>

## [TfIdf](http://radimrehurek.com/gensim/models/tfidfmodel.html):
The TfIdf, term frequency inverse document frequency, is a numerical statistic that is intended to reflect how important a word is to a document in a collection or corpus. The TfIdf value increases proportionally to the number of times a word appears in the document, but is offset by the frequency of the word in the corpus, which helps to control for the fact that some words are generally more common than others. 

To train a model using TfIdf, you first need to go through the corpus once and copute doc frequencies, which we already did above.  

Typically, the TfIdf weight is composed by two terms: the first computes the normalized term frequency, which is the number of times a word appears in a document, divided by the total number of words in that document; the second term is the inverse document frequency (idf), computed as the logarithm of the number of the documents in the corpus divided by the number of documents where the specific term appears.

$$TfIdf = {token\ frequency\ in\ doc} * \ln(\frac{total\ docs\ in\ corpus}{total\ docs\ w/\ token})$$

Tf: Term Frequency, which measures how frequently a term occurs in a document. Since every document is different in length, it is possible that a term would appear much more times in long documents than shorter ones. Thus, the term frequency is often divided by the document length (aka. the total number of terms in the document) as a way of normalization.


Idf: Inverse Document Frequency, which measures how important a term is. While computing Tf, all terms are considered equally important. However it is known that certain terms, such as "is", "of", and "that", may appear a lot of times but have little importance. Thus we need to weigh down the frequent terms while scale up the rare ones, by computing the following: 

<pre>
from gensim import corpora, models, similarities
tfidf = models.TfidfModel(vector_corpus, normalize=False) # trains the model 
print tfidf
corpus_tfidf=tfidf[vector_corpus]
print (dictionary.token2id)
for doc in corpus_tfidf:
    print doc
#   tfidf = (<normalized> term frequency)                                     * (inverse document frequency) 

#   tfidf = (# of instances of word in single doc / # of words in single doc) * ln(# of total documents / # of docs in which word appears) = tfidf

#   the tfidf matrix can be used to convert any vector ( uniq id, count per doc ) to ( uniq id, tfidf score )
</pre>



##Latent Dirichlet Allocation vs Latent Semantic Indexing 

Inerteresting perspective: [link](http://stats.stackexchange.com/questions/32310/topic-models-and-word-co-occurrence-methods)

"I will just describe four milestones/popular models and their advantages/disadvantages and thus highlight (some of) the main differences (or at least what I think are the main/most important differences).

The "easiest" approach, which would be to cluster the documents by matching them against a predefined query of terms (as in PMI). These lexical matching methods however might be inaccurate due to polysemy (multiple meanings) and synonymy (multiple words that have similar meanings) of single terms.

As a remedy, latent semantic indexing (LSI) tries to overcome this by mapping terms and documents into a latent semantic space via a singular value decomposition. The LSI results are more robust indicators of meaning than individual terms would be. However, one drawback of LSI is that it lacks in terms of solid probabilistic foundation.

This was partly solved by the invention of probabilistic LSI (pLSI). In pLSI models each word in a document is drawn from a mixture model specified via multinomial random variables (which also allows higher-order co-occurences as @sviatoslav hong mentioned). This was an important step forward in probabilistic text modeling, but was incomplete in the sense that it offers no probabilistic structure at the level of documents.

Latent Dirichlet Allocation (LDA) alleviates this and was the first fully probabilistic model for text clustering. Blei et al. (2003) show that pLSI is a maximum a-posteriori estimated LDA model under a uniform Dirichlet prior.

Note that the models mentioned above (LSI, pLSI, LDA) have in common that they are based on the “bag-of-words” assumption - i.e. that within a document, words are exchangeable, i.e. the order of words in a document can be neglected. This assumption of exchangeability offers a further justification for LDA over the other approaches: Assuming that not only words within documents are exchangeable, but also documents, i.e., the order of documents within a corpus can be neglected, De Finetti's theorem states that any set of exchangeable random variables has a representation as a mixture distribution. Thus if exchangeability for documents and words within documents is assumed, a mixture model for both is needed. Exactly this is what LDA generally achieves but PMI or LSI do not (and even pLSI not as beautiful as LDA)."

\----

The LSI process transforms documents from TfIdf-weighted space into a latent space of a lower dimensionality.

LDA can be explained using plate notation. The boxes are “plates” representing replicates. The outer plate represents documents, while the inner plate represents the repeated choice of topics and words within a document. 
* M denotes the number of documents
* N the number of words in a document
* α is the parameter of the Dirichlet prior on the per-document topic distributions
* β is the parameter of the Dirichlet prior on the per-topic word distribution
* $\theta_i$ is the topic distribution for document i
* $\phi_k$is the word distribution for topic k
* z_{ij} is the topic for the jth word in document i
* w_{ij} is the specific word.

![](https://github.com/blehman/Data-Science-45min-Intros/blob/master/topic-modeling-101/image.png)


<pre>
from itertools import *
number_of_clusters=3
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=number_of_clusters) # initialize an LSI transformation
lda = models.ldamodel.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=number_of_clusters,\
                               update_every=1, chunksize=10000, passes=1)
corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
corpus_lda = lda[corpus_tfidf] 
# for item in corpus_lsi:
#    print (item)
print "-"*10+"LDA"+"-"*10
t=0
for t, item in enumerate(lda.print_topics(number_of_clusters)):
    print "topic#{0}: {1}".format(t,item)
print
for item in corpus_lda:
    print item
    #print lsi.show_topics()
#print lsi.print_topic(0,topn=1)
# save to disk
#print lsi.projection.s
#lsi.save('corpus_lsi.lsi')
#lsi=models.LsiModel.load
print 
print 
#models.lsimodel.clip_spectrum(0.1,4,discard=0.001)

# Find the threshold, let's set the threshold to be 1/#clusters,
# To prove that the threshold is sane, we average the sum of all probabilities:
scores = list(chain(*[[score for topic,score in topic] \
                      for topic in [doc for doc in corpus_lda]]))
threshold = sum(scores)/len(scores)
print "threshold:",threshold
print
cluster1 = [j for i,j in zip(corpus_lda,documents) if i[0][1] > threshold]
cluster2 = [j for i,j in zip(corpus_lda,documents) if i[1][1] > threshold]
cluster3 = [j for i,j in zip(corpus_lda,documents) if i[2][1] > threshold]

print "topic#0: {0}".format(cluster1)
print "topic#1: {0}".format(cluster2)
print "topic#2: {0}".format(cluster3)

print 
print
print "-"*10+"LSI"+"-"*10
t=0
for t, item in enumerate(lsi.print_topics(number_of_clusters)):
    print "topic#{0}: {1}".format(t,item)
print

for item in corpus_lsi:
    print item
    #print lsi.show_topics()
#print lsi.print_topic(0,topn=1)
# save to disk
#print lsi.projection.s
#lsi.save('corpus_lsi.lsi')
#lsi=models.LsiModel.load
print 
print 
#models.lsimodel.clip_spectrum(0.1,4,discard=0.001)

# Find the threshold, let's set the threshold to be 1/#clusters,
# To prove that the threshold is sane, we average the sum of all probabilities:
scores = list(chain(*[[score for topic,score in topic] \
                      for topic in [doc for doc in corpus_lsi]]))
threshold = sum(scores)/len(scores)
print "threshold:",threshold
print

cluster1 = [j for i,j in zip(corpus_lsi,documents) if i[0][1] > threshold]
cluster2 = [j for i,j in zip(corpus_lsi,documents) if i[1][1] > threshold]
cluster3 = [j for i,j in zip(corpus_lsi,documents) if i[2][1] > threshold]

print "topic#1: {0}".format(cluster1)
print "topic#2: {0}".format(cluster2)
print "topic#3: {0}".format(cluster3)

</pre>


