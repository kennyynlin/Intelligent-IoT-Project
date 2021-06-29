#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 11:26:40 2020

@author: Kenny
"""

import pandas as pd

#Import dataset
dataset = pd.read_csv('dataset_0612.csv')
x = dataset.iloc[:,:-1].values
y = dataset.iloc[:,-1].values

#Encoding categorical data
from sklearn.preprocessing import OneHotEncoder
onehotencoder = OneHotEncoder()
y = y.reshape(-1,1)
y = onehotencoder.fit_transform(y).toarray()

#Splitting the dataset into the training set and test set
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25)

#Feature Scaling
from sklearn.preprocessing import Normalizer
norm_x = Normalizer()
x_train = norm_x.fit_transform(x_train)
x_test = norm_x.transform(x_test)




#Import Keras
from keras.models import Sequential
from keras.layers import Dense

#Initializing the ANN
classifier = Sequential()

#Adding input layer and first hidden layer
classifier.add(Dense(units = 752, activation = 'relu', kernel_initializer = 'uniform', input_dim = 1500))

#Adding the second hidden layer
classifier.add(Dense(units = 752, activation = 'relu', kernel_initializer = 'uniform'))

#Adding the third hidden layer
#classifier.add(Dropout(0.2))
classifier.add(Dense(units = 752, activation = 'relu', kernel_initializer = 'uniform'))

#Adding the forth hidden layer
#classifier.add(Dropout(0.2))
classifier.add(Dense(units = 752, activation = 'relu', kernel_initializer = 'uniform'))

#Adding the output layer
classifier.add(Dense(units = 5, activation = 'softmax', kernel_initializer = 'uniform'))

#Compiling the ANN
classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

#Fitting the ANN to training set
classifier.fit(x_train, y_train, batch_size = 6, epochs = 100)

#Predicting the test set result
y_pred = classifier.predict(x_test)



import pickle
pickle.dump(classifier,open('ANN_Model_0612(4,6,100).pkl','wb'))

import numpy as np

y_pred_cm = []
y_test_cm = []

for i in range(0,225):
    y_pred_cm.append(np.argmax(y_pred[i,:]))
    y_test_cm.append(np.argmax(y_test[i,:]))
    

#Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test_cm, y_pred_cm)
 



    


