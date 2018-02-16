# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from bottle import route, run, request

####

upload_dir = 'predict_upload_files'
coin_imgs_dir = 'predict_coin_imgs'
train_weights_file = 'train_weights.h5'

####

class Plot:

    def __init__(self):
        plt.ion()

        img_blank = np.zeros((150, 150, 3))

        self.img = plt.imshow(img_blank)

        plt.pause(0.1)

    def set_img(self, img):
        self.img.set_data(img)

    def pause(self):
        plt.pause(0.1)

####

plot = Plot()

@route('/upload', method='POST')
def do_upload():
    uploadfrom = request.forms.get('uploadfrom')
    if uploadfrom != 'coin_capture':
        return 'failure'

    upload = request.files.get('picture')
    if not upload.filename.lower().endswith(('.jpg', '.jpeg')):
        return 'failure'

    filepath = 'test.jpg'

    upload.save(filepath, overwrite=True)

    # (h, w, c), c:(r,g,b), c: 0 - 1
    img = plt.imread(filepath)
    plot.set_img(img)
    plot.pause()

    return 'success'

run(host='0.0.0.0', port=8080, debug=True, reloader=False)
