from PIL import Image
import glob
from resizeimage import resizeimage
from keras import backend as K
from six.moves import cPickle
from keras.datasets import cifar10
import numpy as np
import csv
import codecs
import random

import re
r = re.compile("\d+")
def key1(a):
    m = r.findall(a)
    return int(m[0]), int(m[1])

#resize images
def resize_Images():
    for filepath in glob.iglob('dataset/*.jpg'):
        with open(filepath, 'r+b') as f:
            with Image.open(f) as image:
                resized = resizeimage.resize_contain(image, [32, 32])
                resized.save('resized/' + filepath, image.format)

def load_Data():
    num_train_samples = 2274
    testset_size = 450

    x_train = np.empty((num_train_samples, 32, 32, 3), dtype='uint8')
    y_train = np.empty((num_train_samples,), dtype='uint8')

    (all_x, all_y) = load_batch()

    random_choice = random.sample(range(num_train_samples), testset_size)
    rest = np.setdiff1d(range(num_train_samples), random_choice)
  
    y_test = np.take(all_y, random_choice)
    y_train = np.take(all_y, rest)
    
    x_train = []
    x_test = []
    for index in range(num_train_samples):
        if index in random_choice:
	    x_test.append(all_x[index])
	else:
	    x_train.append(all_x[index])
	
    x_train = np.array(x_train)
    x_test = np.array(x_test)	

    y_train = np.reshape(y_train, (len(y_train), 1))
    y_test = np.reshape(y_test, (len(y_test), 1))
    return (x_train, y_train), (x_test, y_test)

def load_batch():
    #image data
    imageCount = 0
    filelist = []
    for imagefile in glob.iglob('dataset/resized_dataset/*.jpg'):
        filelist.append(imagefile)
        imageCount += 1

    filelist.sort(key = key1)
    data = np.zeros((imageCount, 32, 32, 3))
    labels = np.zeros(imageCount)
    index = 0

    for imagefile in filelist:
	print(imagefile)
        t = Image.open(imagefile)
        arr = np.array(t) #Convert test image into an array 32*32*3    
        data[index] = arr 
        index += 1
        
    #labels
    labels = []
    #for filepath in glob.iglob(''):
    with open('dataset/labels/all.txt') as csvfile:
        lines = csvfile.readlines()
        for line in lines:
            labels.append(line.strip().split(',')[1])    
    return data, labels

