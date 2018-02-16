# -*- coding: utf-8 -*-

import os
import random
import shutil

####

manual_classified_coin_imgs_dir = 'manual_classified_coin_imgs'
data_dir = 'data'

####

def copy_data(class_name):
    imgs_dir = os.path.join(manual_classified_coin_imgs_dir, class_name)

    train_dir = os.path.join(data_dir, os.path.join('train', class_name))
    validation_dir = os.path.join(data_dir, os.path.join('validation', class_name))

    os.makedirs(validation_dir, exist_ok=True)
    os.makedirs(train_dir, exist_ok=True)

    files = os.listdir(imgs_dir)
    random.shuffle(files)

    # 1 割を検証用とする
    num_validation = len(files)//10

    for i in range(0, num_validation):
        shutil.copyfile(os.path.join(imgs_dir, files[i]), os.path.join(validation_dir, files[i]))

    for i in range(num_validation, len(files)):
        shutil.copyfile(os.path.join(imgs_dir, files[i]), os.path.join(train_dir, files[i]))

####

shutil.rmtree(data_dir, ignore_errors=True)

copy_data('head')
copy_data('tail')
copy_data('other')


