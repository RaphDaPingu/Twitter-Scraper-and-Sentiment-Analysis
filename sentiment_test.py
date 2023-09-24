import numpy as np
import pandas as pd

dataset = pd.read_excel("tweets_test.xlsx")
#dataset = pd.read_excel("tweets_train.xlsx")
print(dataset)

import re
import nltk

nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

all_stopwords = stopwords.words('english')
all_stopwords.remove('not')

corpus = []

for i in range(0, len(dataset)):
  tweet = re.sub('[^a-zA-Z]', ' ', dataset['Tweets'][i])
  tweet = tweet.split()
  tweet = [ps.stem(word) for word in tweet if not word in set(all_stopwords)]
  tweet = ' '.join(tweet)
  corpus.append(tweet)

print(corpus)
  
# Loading BoW dictionary
from sklearn.feature_extraction.text import CountVectorizer
import pickle
cvFile='sentiment_model.pkl'
cv = pickle.load(open(cvFile, "rb"))

import joblib
classifier = joblib.load('twitter_classifier')

X_fresh = cv.transform(corpus).toarray()
print(X_fresh.shape)

y_pred = classifier.predict(X_fresh)
print(y_pred)

dataset['Predicted'] = y_pred.tolist()
print(dataset)

### If there exists a dataset with human-tagged "Attitude" column, uncomment this (tweets_train_online_resource can use tweets_train as test, tweets_train can use tweets_test as test):
##
##attitude = dataset['Attitude'].tolist()
##predicted = y_pred.tolist()
##
##print(attitude)
##print(predicted)
##
##matching = 0
##actual = len(dataset)
##
##for i in range(len(dataset)):
##  if (attitude[i] == predicted[i]):
##    matching += 1
##
##print(str(matching) + "/" + str(actual))
##print(str((matching / actual) * 100) + "%")
