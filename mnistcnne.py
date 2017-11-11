'''this trains a conv net by increasing the hyper parameters(number of feature layers)
and draws a graph to justify the number of features
'''
from __future__ import print_function
import sys
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from matplotlib import pyplot as plt

sys.stdout = open("accuracy_log.txt", "w")

batch_size = 128
num_classes = 62
epochs = 1

# input image dimensions
img_rows, img_cols = 28, 28

# the data, shuffled and split between train and test sets
fp1 = open('dataset1.pkl', 'r')
fp2 = open('dataset2.pkl','r')


[x_train, y_train],[x_vladation, y_validation], [x_test, y_test] = cPickle.load(fp1)
[p_train, q_train],[p_vladation, q_validation], [p_test, q_test] = cPickle.load(fp2)

x_train = x_train.extend(p_train)
y_train = y_train.extend(y_train)

if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

accuracies = []
count = 10
for i in range(count):

	model = Sequential()
	model.add(Conv2D((16+2*i), kernel_size=(5, 5),
	                 activation='relu',
	                 input_shape=input_shape))
	model.add(MaxPooling2D(pool_size=(2,2)))
	model.add(Conv2D((16+i*2)*2, (3, 3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.25))
	model.add(Flatten())
	model.add(Dense(1000, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(1000, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(num_classes, activation='softmax'))

	model.compile(loss=keras.losses.categorical_crossentropy,
	              optimizer=keras.optimizers.Adadelta(),
	              metrics=['accuracy'])

	model.fit(x_train, y_train,
	          batch_size=batch_size,
	          epochs=epochs,
	          verbose=1,
	          validation_data=(x_test, y_test))
	score = model.evaluate(x_test, y_test, verbose=0)
	print('Test loss:', score[0])
	print('Test accuracy:', score[1])
	accuracies.append(score[1])

plt.plot([x for x in range(count)], accuracies,'r--')
plt.show()

