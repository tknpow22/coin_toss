# -*- coding: utf-8 -*-

import os
import shutil
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from common import Common, MyModel

####

test_coin_imgs_dir = 'test_coin_imgs'
auto_classified_coin_imgs_dir = 'test_classified_coin_imgs'
train_weights_file = 'train_weights.h5'

####

model = MyModel.get_model()
model.summary()

model.load_weights(train_weights_file)
print('load_weights:', train_weights_file)

shutil.rmtree(auto_classified_coin_imgs_dir, ignore_errors=True)
files = os.listdir(test_coin_imgs_dir)

for file in files:

    if not file.lower().endswith(('.jpg', '.jpeg')):
        continue

    img = load_img(os.path.join(test_coin_imgs_dir, file), target_size=Common.INPUT_SHAPE)
    x = img_to_array(img)
    x /= 255.0

    x = np.expand_dims(x, axis=0)

    preds = model.predict(x)

    class_index = np.argmax(preds)
    class_name = Common.CLASSES[class_index]

    class_dir = os.path.join(auto_classified_coin_imgs_dir, class_name)
    os.makedirs(class_dir, exist_ok=True)

    shutil.copyfile(os.path.join(test_coin_imgs_dir, file), os.path.join(class_dir, file))
