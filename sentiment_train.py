import numpy as np
import pandas as pd

dataset = pd.read_csv("tweets_train_online_resource.csv", encoding="latin-1")
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
  tweet = tweet.lower()
  tweet = tweet.split()
  tweet = [ps.stem(word) for word in tweet if not word in set(all_stopwords)]
  tweet = ' '.join(tweet)
  corpus.append(tweet)

print(corpus)
  
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 1420)

X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, -1].values

# Saving BoW dictionary to later use in prediction
import pickle
bow_path = 'sentiment_model.pkl'
#bow_path = 'sentiment_model_worse.pkl'
pickle.dump(cv, open(bow_path, "wb"))

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Exporting NB Classifier to later use in prediction
import joblib
joblib.dump(classifier, 'twitter_classifier')
#joblib.dump(classifier, 'twitter_classifier_worse')

y_pred = classifier.predict(X_test)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)

print(accuracy_score(y_test, y_pred))
