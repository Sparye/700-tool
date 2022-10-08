import tensorflow as tf
from tensorflow.python.keras.layers import  Dense
from tensorflow.python.keras.models import Sequential
from keras.utils import np_utils

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

x_train = x_train.reshape((x_train.shape[0], 28*28)).astype('float32')
x_test = x_test.reshape((x_test.shape[0], 28*28)).astype('float32')
x_train = x_train / 255
x_test = x_test / 255


y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)

model = Sequential()

model.add(Dense(32,input_dim=28*28,activation='sigmoid'))
model.add(Dense(64,activation='relu'))
model.add(Dense(64,activation='sigmoid'))
model.add(Dense(64,activation='relu'))
model.add(Dense(64,activation='sigmoid'))
model.add(Dense(64,activation='relu'))
model.add(Dense(64,activation='sigmoid'))
model.add(Dense(64,activation='relu'))
model.add(Dense(64,activation='sigmoid'))
model.add(Dense(64,activation='relu'))
model.add(Dense(10,activation='softmax'))
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

h1 = model.fit(x_train, y_train, batch_size=100, epochs=20,verbose=2)

model.evaluate(x_test,y_test)


