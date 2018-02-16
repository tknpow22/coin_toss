# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from common import Common, MyModel

####

train_weights_file = 'train_weights.h5'

####

def parse_args():
    argparser = ArgumentParser()

    argparser.add_argument('-f', '--file',
                           required=True,
                           action='store',
                           type=str,
                           help='coin image path')

    return argparser.parse_args()

####

args = parse_args()

model = MyModel.get_model()
model.summary()

model.load_weights(train_weights_file)
print('load_weights:', train_weights_file)

img = load_img(args.file, target_size=Common.INPUT_SHAPE)
x = img_to_array(img)
x /= 255.0

x = np.expand_dims(x, axis=0)

preds = model.predict(x)
print(preds)

class_index = np.argmax(preds)
class_name = Common.CLASSES[class_index]
print(class_name)

