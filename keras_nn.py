import keras
import numpy as np
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense

#loading the data set
dataset = loadtxt('OHEEPD.csv', delimiter=',')
#splitting hte datat into x and y vars
#print(dataset)
x=dataset[:,0:22]
y=dataset[:,22:27]
#defieing keras model
model = Sequential()
model.add(Dense(64, input_dim=22, activation='relu'))#creating model that expects rows of data with 19 vars and this is 1st hidden layer has 12 nodes uses relu activaiton funciton
model.add(Dense(32,activation ='relu'))#2nd hidden layer has 8 nodes and relu activaiton function
model.add(Dense(32,activation ='relu'))#3nd hidden layer has 8 nodes and relu activaiton function
model.add(Dense(16,activation ='relu'))#4th hidden layer has 8 nodes and relu activaiton function
model.add(Dense(5, activation='sigmoid'))# output layer has 1 node uses sigmoid activaiton funciton

#Complie the Keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#fit the model 
#epoch-one pass through of all of the rows in a training set(one epoch is made of 1 or more batches)
#batch-one or more samples considered by the model within an epoch before weights are updated
model.fit(x,y, epochs=100, batch_size=50)

#evaluate the model
_, accuracy = model.evaluate(x,y)
print('Accuracy: %2f' %(accuracy*100))

#saving the model 
model.save("eTriage_model")