import sys

sys.path.insert(0, '../convnets-keras') #not quite sure what this does

from keras import backend as K
import tensorflow as tf
from keras.models import Model
from keras.layers import Flatten, Dense, Dropout, Reshape, Permute, Activation, \
    Input, merge, Lambda
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from convnetskeras.customlayers import convolution2Dgroup, crosschannelnormalization, \
    splittensor, Softmax4D


def mean_subtract(img):
    return tf.image.per_image_standardization(img)
#https://www.tensorflow.org/api_docs/python/tf/image/per_image_standardization


def get_alexnet(input_shape, nb_classes, mean_flag,fc_flag):
    # code adapted from https://github.com/heuritech/convnets-keras

    inputs = Input(shape=input_shape)

    if mean_flag:
        mean_subtraction = Lambda(mean_subtract, name='mean_subtraction')(inputs)
        conv_1 = Convolution2D(96, 11, 11, subsample=(4, 4), activation='relu',
                               name='conv_1', init='he_normal')(mean_subtraction)
    else:
        conv_1 = Convolution2D(96, 11, 11, subsample=(4, 4), activation='relu',
                               name='conv_1', init='he_normal')(inputs)
        conv_1 = Conv2D(96,(11,11),strides=(4,4),activation='relu',name='conv_1',kernel_initializer='he_normal')

    conv_2 = MaxPooling2D((3, 3), strides=(2, 2))(conv_1)
    conv_2 = crosschannelnormalization(name="convpool_1")(conv_2)
    conv_2 = ZeroPadding2D((2, 2))(conv_2)
    conv_2 = merge([
                       Convolution2D(128, 5, 5, activation="relu", init='he_normal', name='conv_2_' + str(i + 1))(
                           splittensor(ratio_split=2, id_split=i)(conv_2)
                       ) for i in range(2)], mode='concat', concat_axis=1, name="conv_2")

    conv_3 = MaxPooling2D((3, 3), strides=(2, 2))(conv_2)
    conv_3 = crosschannelnormalization()(conv_3)
    conv_3 = ZeroPadding2D((1, 1))(conv_3)
    conv_3 = Convolution2D(384, 3, 3, activation='relu', name='conv_3', init='he_normal')(conv_3)

    conv_4 = ZeroPadding2D((1, 1))(conv_3)
    conv_4 = merge([
                       Convolution2D(192, 3, 3, activation="relu", init='he_normal', name='conv_4_' + str(i + 1))(
                           splittensor(ratio_split=2, id_split=i)(conv_4)
                       ) for i in range(2)], mode='concat', concat_axis=1, name="conv_4")

    conv_5 = ZeroPadding2D((1, 1))(conv_4)
    conv_5 = merge([
                       Convolution2D(128, 3, 3, activation="relu", init='he_normal', name='conv_5_' + str(i + 1))(
                           splittensor(ratio_split=2, id_split=i)(conv_5)
                       ) for i in range(2)], mode='concat', concat_axis=1, name="conv_5")

    dense_1 = MaxPooling2D((3, 3), strides=(2, 2), name="convpool_5")(conv_5)

    dense_1 = Flatten(name="flatten")(dense_1)

    if(fc_flag):
        dense_1 = Dense(4096, activation='relu', name='dense_1_new', init='he_normal')(dense_1)
    else
        dense_1 = Dense(4096, activation='relu', name='dense_1', init='he_normal')(dense_1)

    dense_2 = Dropout(0.5)(dense_1)

    if(fc_flag):
        dense_2 = Dense(4096, activation='relu', name='dense_2_new', init='he_normal')(dense_2)
    else:
        dense_2 = Dense(4096, activation='relu', name='dense_2', init='he_normal')(dense_2)

    dense_3 = Dropout(0.5)(dense_2)
    dense_3 = Dense(nb_classes, name='dense_3_new', init='he_normal')(dense_3)

    prediction = Activation("softmax", name="softmax")(dense_3)

    alexnet = Model(input=inputs, output=prediction)

    return alexnet
