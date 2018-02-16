# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from bottle import route, run, request
from keras.preprocessing.image import img_to_array, load_img
from common import Common, CoinImage, MyModel

####

upload_dir = 'predict_upload_files'
coin_imgs_dir = 'predict_coin_imgs'
train_weights_file = 'train_weights.h5'

####

class Plot:

    def __init__(self):
        plt.ion()
        figure = plt.figure()

        axes_orig = figure.add_subplot(1,2,1)
        self.axes_coin = figure.add_subplot(1,2,2)

        img_orig_blank = np.zeros((Common.UPLOAD_IMG_HEIGHT, Common.UPLOAD_IMG_WIDTH, Common.COLORS))
        self.img_coin_blank = np.zeros((Common.IMG_HEIGHT, Common.IMG_WIDTH, Common.COLORS))

        self.axes_img_orig = axes_orig.imshow(img_orig_blank)
        self.axes_img_coin = self.axes_coin.imshow(self.img_coin_blank)

        plt.pause(0.1)

    def set_orig_img(self, img):
        self.axes_img_orig.set_data(img)

    def set_coin_img(self, img):
        self.axes_img_coin.set_data(img)

    def set_blank_coin_img(self):
        self.axes_img_coin.set_data(self.img_coin_blank)

    def set_coin_title(self, title):
        self.axes_coin.set_title(title)

    def pause(self):
        plt.pause(0.1)

####

model = MyModel.get_model()
model.summary()

model.load_weights(train_weights_file)
print('load_weights:', train_weights_file)

plot = Plot()

@route('/upload', method='POST')
def do_upload():
    uploadfrom = request.forms.get('uploadfrom')
    if uploadfrom != 'coin_capture':
        return 'failure'

    upload = request.files.get('picture')
    if not upload.filename.lower().endswith(('.jpg', '.jpeg')):
        return 'failure'

    filepath = os.path.join(upload_dir, upload.filename)

    upload.save(filepath)

    # (h, w, c), c:(r,g,b), c: 0 - 1
    img_orig = plt.imread(filepath)
    plot.set_orig_img(img_orig)

    # (h, w, c), c:(b,g,r), c: 0 - 255
    cimg = CoinImage.get_img(filepath)
    if cimg is not None:
        coin_filepath = os.path.join(coin_imgs_dir, upload.filename)

        cv2.imwrite(coin_filepath, cimg)

        # (h, w, c), c:(r,g,b), c: 0 - 1
        img_coin = plt.imread(coin_filepath)
        plot.set_coin_img(img_coin)

        img = load_img(coin_filepath, target_size=Common.INPUT_SHAPE)
        # (h, w, c), c:(r,g,b), c: 0 - 255
        x = img_to_array(img)
        x /= 255.0

        x = np.expand_dims(x, axis=0)

        preds = model.predict(x)
        print(preds)

        class_index = np.argmax(preds)
        class_name = Common.CLASSES[class_index]

        plot.set_coin_title(class_name)

    else:
        plot.set_blank_coin_img()
        plot.set_coin_title('no image')

    plot.pause()

    return 'success'

run(host='0.0.0.0', port=8080, debug=True, reloader=False)
