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

We can optimize k before we use kNN. This technique usually involves something like k-folds and testing various values of k, which let's us compare the mean error rates and choose "the best" k-value.   

An alternative approach: optimize k while we use kNN. What if we let k vary (for each unknown) depending on the distribution of distances? A simple application would be to calculate all distances and k to be the number of neighbors within 1 standard deviation from the mean distance. 

In summary, optimizing k is a great idea; I don't have a great answer for you, but many people seem to like k-folds cross validation [[reference paper](http://lshtc.iit.demokritos.gr/system/files/XiaogangHan.pdf)]. I like the idea of letting k vary based on the relationship between the unknown datum and the labeled neighbors. 

### Distance calculation
We can use euclidean distance or something differnt like using curved space. This choice is important as it directly orders the "nearness" of the neighbors. 

The main drawback to using kNN is that it can be rather huge memory suck.  

### Label Logic
A typical technique is to organize the k neariest neighbors labels as votes towards a certain label. The candidate with the most votes could win, but the label returned is entirely up to the author of the technique. 
