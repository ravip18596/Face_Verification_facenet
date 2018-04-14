
# coding: utf-8

# # Face Recognition for the Attendence System
# 
# Face recognition problems commonly fall into two categories: 
# 
# - **Face Verification** - "is this the claimed person?". For example, at some airports, you can pass through customs by letting a system scan your passport and then verifying that you (the person carrying the passport) are the correct person. A mobile phone that unlocks using your face is also using face verification. This is a 1:1 matching problem. 
# - **Face Recognition** - "who is this person?". For example, the video lecture showed a face recognition video (https://www.youtube.com/watch?v=wr4rx0Spihs) of Baidu employees entering the office without needing to otherwise identify themselves. This is a 1:K matching problem. 
# 
# FaceNet learns a neural network that encodes a face image into a vector of 128 numbers. By comparing two such vectors, you can then determine if two pictures are of the same person.
#     
# - Implement the triplet loss function
# - Use a pretrained model to map face images into 128-dimensional encodings
# - Use these encodings to perform face verification and face recognition
# 
# We will be using a pre-trained model which represents ConvNet activations using a "channels first" convention, as opposed to the "channels last" convention used in lecture and previous programming assignments. In other words, a batch of images will be of shape $(m, n_C, n_H, n_W)$ instead of $(m, n_H, n_W, n_C)$. Both of these conventions have a reasonable amount of traction among open-source implementations; there isn't a uniform standard yet within the deep learning community. 
# 
# Let's load the required packages. 


# In[3]:


from keras.models import Sequential
from keras.layers import Conv2D, ZeroPadding2D, Activation, Input, concatenate
from keras.models import Model,load_model
from keras.layers.normalization import BatchNormalization
from keras.layers.pooling import MaxPooling2D, AveragePooling2D
from keras.layers.merge import Concatenate
from keras.layers.core import Lambda, Flatten, Dense
from keras.initializers import glorot_uniform
from keras.engine.topology import Layer
from keras import backend as K
K.set_image_data_format('channels_first')
import cv2
import os
import numpy as np
from numpy import genfromtxt
#import pandas as pd
import tensorflow as tf
from fr_utils import *
from inception_blocks import *
#
# np.set_printoptions(threshold=np.nan)
#
#
#FRmodel = faceRecoModel(input_shape=(3, 96, 96))
#
#
# # In[5]:
#
#
# print("Total Params:", FRmodel.count_params())
#
#
class FaceNetModel:

    def __init__(self):
        self.FRmodel = faceRecoModel(input_shape=(3, 96, 96))
        self.FRmodel.compile(optimizer = 'adam', loss = self.triplet_loss, metrics = ['accuracy'])
        load_weights_from_FaceNet(self.FRmodel)

    def triplet_loss(self,y_true, y_pred, alpha = 0.2):
        """
        Implementation of the triplet loss as defined by formula (3)

        Arguments:
        y_true -- true labels, required when you define a loss in Keras, you don't need it in this function.
        y_pred -- python list containing three objects:
                anchor -- the encodings for the anchor images, of shape (None, 128)
                positive -- the encodings for the positive images, of shape (None, 128)
                negative -- the encodings for the negative images, of shape (None, 128)

        Returns:
        loss -- real number, value of the loss
        """

        anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]

        ### START CODE HERE ### (≈ 4 lines)
        # Step 1: Compute the (encoding) distance between the anchor and the positive
        pos_dist =  tf.reduce_sum(tf.square(tf.subtract(anchor,positive)),axis=-1)
        # Step 2: Compute the (encoding) distance between the anchor and the negative
        neg_dist = tf.reduce_sum(tf.square(tf.subtract(anchor,negative)),axis=-1)
        # Step 3: subtract the two previous distances and add alpha.
        basic_loss = tf.add(tf.subtract(pos_dist,neg_dist),alpha)
        # Step 4: Take the maximum of basic_loss and 0.0. Sum over the training examples.
        loss = tf.reduce_sum(tf.maximum(basic_loss,0))
        ### END CODE HERE ###

        return loss



    def returnModel(self):
        return self.FRmodel


    def verify(self,image_path, stored_encoding):
        """
        Function that verifies if the person on the "image_path" image is "identity".
        
        Arguments:
        image_path -- path to an image
        identity -- string, name of the person you'd like to verify the identity. Has to be a resident of the Happy house.
        database -- python dictionary mapping names of allowed people's names (strings) to their encodings (vectors).
        model -- your Inception model instance in Keras
        
        Returns:
        dist -- distance between the image_path and the image of "identity" in the database.
        door_open -- True, if the door should open. False otherwise.
        """
        
        ### START CODE HERE ###
        
        # Step 1: Compute the encoding for the image. Use img_to_encoding() see example above. (≈ 1 line)
        encoding = img_to_encoding(image_path=image_path,model=self.FRmodel)
        
        # Step 2: Compute distance with identity's image (≈ 1 line)
        dist = np.linalg.norm(encoding - stored_encoding)
        
        # Step 3: Open the door if dist < 0.7, else don't open (≈ 3 lines)
        '''        
        if dist<0.85:
            print("It's " + str(identity) + ", welcome home!")
            door_open = True
        else:
            print("It's not " + str(identity) + ", please go away")
            door_open = False
        '''            
        ### END CODE HERE ###
            
        return dist




#
# verify("images/camera_0.jpg", "younes", database, FRmodel)
#
#
# verify("images/camera_2.jpg", "kian", database, FRmodel)
#
# database["Ravi"] = img_to_encoding("images/rp1.jpg",FRmodel)
#
#
#
# verify("images/rp2.jpeg","Ravi",database,FRmodel)
#
#
#
# verify("images/rishabh.jpeg","Ravi",database,FRmodel)




