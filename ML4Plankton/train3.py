'''
Finetuning from pre-trained AlexNet weights - ONLY TRAINING FULLY CONNECTED LAYERS
'''

from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import SGD
import os

from alexnet_base import *
from utils import *


#set hyperparameters + image parameters
batch_size = 16
height = 277
width = 277
input_size = (3,height,width)
num_classes = 2
mean_flag = True    #perform mean subtraction on images in AlexNet
fc_flag = True      #don't load weights for fully_connected layers

weights_path = 'convnets-keras/weights/alexnet_weights.h5'
train_path = 'data/train'
validation_path = 'data/test'

samples_per_epoch = len(os.listdir(train_path))    #total number of images in training set = images per epoch
nb_val_samples = len(os.listdir(validation_path))    #total number of images in validation set
nb_epoch = 50

#create data generators for train and test sets
train_datagen = ImageDataGenerator()
validation_datagen = ImageDataGenerator()

train_generator = train_datagen.flow_from_directory(
    train_path,
    batch_size=batch_size,
    target_size=(height,width),
    class_mode='binary')

validation_generator = validation_datagen.flow_from_directory(
    validation_path
    batch_size = batch_size,
    target_size = (height, width),
    class_mode = 'binary')

#build AlexNet model
alexnet = get_alexnet(input_size,num_classes,mean_flag,fc_flag)
#load pre-trained weights
alexnet.load_weights(weights_path, by_name=True)

#freeze convolutional layers, unfreeze all dense layers
alexnet = unfreeze_layer_onwards(alexnet, 'dense_1_new')

#create optimizer
sgd = SGD(lr=0.01,decay=1e-6,momentum=0.9,nesterov=True)
#configure learning process
alexnet.compile(loss='binary_crossentropy',
                optimizer=sgd,
                metrics=['accuracy'])
#train model
history = alexnet.fit_generator(train_generator,
                      samples_per_epoch=samples_per_epoch,
                      validation_data=validation_generator,
                      nb_val_samples=nb_val_samples,
                      nb_epoch=nb_epoch,
                      verbose=1)

plot_performance(history)