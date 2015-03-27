# k Nearest Neighbors 
We are going to learn how to label some unlabled data based on *similar* characterisitcs to labled data. In terms of vocabulary, we are going to create a classifier for a specific target variable using feature comparisons. 

The starting point is the labeled dataset with various features. In this n-dimensional space, we then caluculate the distance between our unknown datum and it's k closests neighbors. 

The process has three main parts:

- Optimize k
- Distance calculation
- Lablel logic

This tutorial is uses two main resources:
 - [Machine Learning In Action](http://www.manning.com/pharrington/)
 - [Scikit-learn KNeighborsClassifier](http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html)

### Optimize k
A common question: Since k is an input, how do we choose the size of k?

We can optimize k before we use kNN. This technique usually involves something like n-folds and testing various values of k, which let's us compare the mean error rates and choose "the best" k-value.   

An alternative approach: optimize k while we use kNN. What if we let k vary (for each unknown) depending on the distribution of distances? A simple application would be to calculate all distances and k to be the number of neighbors within 1 standard deviation from the mean distance. 

In summary, optimizing k is a great idea. I don't have a great answer for you, but many people seem to like n-folds cross validation [[reference paper](http://lshtc.iit.demokritos.gr/system/files/XiaogangHan.pdf)].  

### Distance calculation
We can use euclidean distance.

Alternatively, we could measure distance using something like using curved space. The scikit-learn package has [various options](http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.DistanceMetric.html#sklearn.neighbors.DistanceMetric).

(*add example code*)

The method for compute distance is an important choice since it directly quantifies the values used in the logic to determine "nearness" of the neighbors. 

This computation can also be the source of major memory issues. If we can recognize those points "closer" to the unknown without computing and storing distances for the entire dataset, then we can drastically improve the performace of kNN.  

### Label Logic
Several questions can be considered while building the logic of labeling the unknown using kNN:
- When a tie vote occors, which label should be selected?
- Should those lables of *closer* nearest neighbors be weighted? 
- How should votes be counted? 
- Is the return value a confidence score for each label? 

A typical technique is to organize the k neariest neighbors labels as votes towards a certain label. The candidate with the most votes could win. 

However, the decision making behind the label returned is entirely up to the author of the technique. 
