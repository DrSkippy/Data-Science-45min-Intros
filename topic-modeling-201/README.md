# Topic Modeling
We'll pull in data from Twitter's public api, parse out the tweet text,
separate the text into a test/training set, vectorize our data, reduce
the number of dimensions using SVD, then build a model that can be used
to label new tweets.  
# Twitter Public API
Let's grab some json records from Twitter's public api that we'll grab
using a package called `python-twitter.`
<pre>
$ pip install python-twitter
$ pydoc twitter.Api
</pre>

Build an app [https://apps.twitter.com/](https://apps.twitter.com/).  

Then use the app info in the `config.cfg` file.
### Train/Test set
Split the training and test set.

### Vectorize the Tweets
Two steps:  
1.  Set up a vectorizer.
2.  Vectorize the tweets to build the vocabulary.

### Dimension Reduction

To choose the appropriate number of svd components, we need to explore the amount of variance explained with each component. We'll reduce the number of components to 600. This number provides about 90% of the explained variance. 

### Create Cluster Centroids
We'll now apply kmeans to find the centroids that will be used to predict a cluster for each tweet.

### Explore Word Loadings
Those tweets nearest the cluster centers are used as an approximation for their meanings.

### Label New Tweets
Apply the model to the test set.

### Test the Results
Each time we apply kmeans, we may have some variation in the results. Developing some consistency in these results could align with the goals of our work. Below are some considerations.

1.) Review the stability of distribution of the labels on the test set. If we re-run the process, does the distribution change dramatically?  
2.) Review the "meaning" of the word loadings. Does the choice of k can largely affect terms?  
3.) Consider new features. Start broad and then use SVD to narrow your selection.  
