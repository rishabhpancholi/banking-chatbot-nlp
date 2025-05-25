# importing necessary libraries

#for data manipulation
import json
import numpy as np
import pandas as pd

#for text preprocessing
import re
import nltk
from nltk.stem import PorterStemmer

# for model training and evaluation
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer,ENGLISH_STOP_WORDS
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
import random


#other modules
import warnings
warnings.filterwarnings('ignore')

#stop words
stop_words= ENGLISH_STOP_WORDS

# loading the json file
with open('banking.json') as f:
    banking = json.load(f)

# getting the inputs and outputs
inputs= [example['text'] for example in banking]
tags = [example['category'] for example in banking]

# preprocessing inputs
ps = PorterStemmer()

for i in range(len(inputs)):
    input = re.sub(r'[^A-Za-z0-9\s]','',inputs[i]) 
    input_words = input.split()
    input_words = [word for word in input_words if word not in stop_words]
    input_words = [ps.stem(word.lower()) for word in input_words]

    inputs[i] = ' '.join(input_words)

# unique list of classes
classes = sorted(list(set(tags)))


# encoding of tags
encoded_tags = []
for tag in tags:
    encoded_tag = [0]*len(classes)
    encoded_tag[classes.index(tag)]=1

    encoded_tags.append(encoded_tag)

# final appending of feature and label
data = []
for i in range(len(inputs)):
    data.append([inputs[i],encoded_tags[i]])

random.shuffle(data)
data = np.array(data,dtype = object)

# seperating the training and testing data
X = np.array([i[0] for i in data])
y = np.array([i[1] for i in data])

# vectorizor initialization
cv = CountVectorizer(ngram_range=(1,2))

# Convert one-hot encoded y to 1D class labels
y=np.argmax(y,axis=1)

#train test split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

# Running algorithm for classification
final_model = LogisticRegression(multi_class='multinomial')
final_model.fit(X_train,y_train)
y_train_pred = final_model.predict(X_train)
y_pred = final_model.predict(X_test)
print(f'The training accuracy score is {accuracy_score(y_train,y_train_pred)}')
print(f'The testing accuracy score is {accuracy_score(y_test,y_pred)}')

with open('chatbot.pkl','wb') as f:
    pickle.dump(final_model,f)

with open('classes.pkl','wb') as f:
    pickle.dump(classes,f)