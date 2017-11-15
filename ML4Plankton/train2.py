'''
Finetuning from pre-trained AlexNet weights - progressive unfreezing of layers
'''

from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import SGD
import os

from alexnet_base import *
from utils import *


#set hyperparameters + image parameters
batch_size = 16
height = 227
width = 227
input_size = (3,height,width)
num_classes = 2
mean_flag = True    #perform mean subtraction on images in AlexNet
fc_flag = False     #load weights from fully_connected layers

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
    validation_path,
    batch_size = batch_size,
    target_size = (height, width),
    class_mode = 'binary')

#build AlexNet model
alexnet = get_alexnet(input_size,num_classes,mean_flag,fc_flag=fc_flag)
alexnet.load_weights(weights_path, by_name=True)


#DECIDE HOW MANY LAYERS TO UNFREEZE
layers = ['dense_3_new', 'dense_2', 'dense_1', 'conv_5_1', 'conv_4_1', 'conv_3', 'conv_2_1', 'conv_1']
epochs = [10, 10, 10, 10, 10, 10, 10, 10]
lr = [1e-2, 1e-3, 1e-3, 1e-3, 1e-3, 1e-3, 1e-3, 1e-3]

history_finetune = []

for i, layer in enumerate(layers):
    alexnet = unfreeze_layer_onwards(alexnet, layer)

    sgd = SGD(lr=lr[i], decay=1e-6, momentum=0.9, nesterov=True)
    alexnet.compile(loss='mse',
                    optimizer=sgd,
                    metrics=['accuracy'])

    for epoch in range(epochs[i]):
        h = alexnet.fit_generator(train_generator,
                                        samples_per_epoch = samples_per_epoch,
                                        validation_data = validation_generator,
                                        nb_val_samples = nb_val_samples,
                                        nb_epoch = nb_epoch,
                                        verbose = 1)
        history_finetune = append_history(history_finetune, h)

plot_performance(history_finetune)
