
# coding: utf-8

# In[1]:

import matplotlib.pyplot as plt
from sklearn.datasets import load_files
from sklearn import datasets
import numpy as np
get_ipython().magic(u'matplotlib inline')



# setting graph parameters

plt.rcParams['figure.figsize'] = 10,7.2
plt.rcParams['axes.grid'] = True
plt.gray()


# In[2]:

# loading text data and extracting data to train our model and test our model

categories = ['alt.atheism','sci.space','talk.religion.misc','comp.graphics']

Train_subset = load_files('datasets/20news-bydate/20news-bydate-train',categories=categories, encoding='latin -1')
Test_subset = load_files('datasets/20news-bydate/20news-bydate-test',categories=categories, encoding='latin -1')

Train_subset.target.shape 
len(Train_subset.data)


# In[43]:

count = 0
for i in Test_subset.data:
    count = count + 1
count    


# In[140]:

#Vectorizing the Training data
from sklearn.feature_extraction.text import TfidfVectorizer 
Vectorizer = TfidfVectorizer(min_df=2)
X_train = Vectorizer.fit_transform(Train_subset.data)
y_train = Train_subset.target

#inner dimmensions agree
print X_train.shape[0] == y_train.shape[0]
print X_train.shape
print y_train


# In[141]:

#training the model using Naive Bayes Classifier
from sklearn.naive_bayes import MultinomialNB

#train classifier and get score
clf = MultinomialNB(alpha=1).fit(X_train,y_train)
print ('Train score:{0:.1f}%'.format(clf.score(X_train,y_train)*100))


# In[156]:

#test classifier and get score (slight over fitting)
X_test = Vectorizer.transform(Test_subset.data[:1])
y_test = Test_subset.target

#print ('Test score:{0:.1f}%'.format(clf.score(X_test,y_test)*100))
X_test


# In[7]:

# Demensionality Reduction and Visualization
from sklearn.decomposition import RandomizedPCA
from itertools import cycle

X_train_pca = RandomizedPCA(n_components=2).fit_transform(X_train)
target_names = Train_subset.target_names
colors = ['r','g','b','y','m','c'] 

for i,c in zip(set(y_train),colors):
    plt.scatter(X_train_pca[y_train == i,0],X_train_pca[y_train == i,1],c=c,label=target_names[i])
plt.legend(loc='best')    

    


# In[8]:

# Model Performance
from sklearn.metrics import classification_report,confusion_matrix

print classification_report(Test_subset.target,clf.predict(X_test),target_names=target_names)


# In[9]:

Test_subset.target


# In[62]:

from boilerpipe.extract import Extractor
from sklearn.feature_extraction.text import CountVectorizer
    


# In[194]:

page = Extractor(extractor='ArticleExtractor', url='http://www.cgsociety.org/')


# In[195]:

page_text = page.getText()
list_page = [page_text]
list_page


# In[196]:


X_test_url = Vectorizer.transform(list_page)
type(Train_subset.data[:1])


# In[197]:

bob = clf.predict(X_test_url)


# In[181]:

#c = 0
#for i in Test_subset.data:
  #   print type(i)
#c        


# In[198]:

bob


# In[173]:

X_test_url


# In[158]:

Test_subset.data[:1] == Test_subset.data[1]


# In[160]:

re = [1,2,3,4,5]
re[:1] == re[0]


# In[188]:

Test_subset.target_names[1]


# In[ ]:



