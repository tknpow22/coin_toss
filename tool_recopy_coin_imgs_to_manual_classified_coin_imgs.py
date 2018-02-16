# -*- coding: utf-8 -*-

import os
import shutil

####

coin_imgs_dir = 'coin_imgs'
manual_classified_coin_imgs_dir = 'manual_classified_coin_imgs'

####

def recopy(subdir):

    category_dir = os.path.join(manual_classified_coin_imgs_dir, subdir)

    files = os.listdir(category_dir)

    for file in files:
        if not os.path.isfile(os.path.join(coin_imgs_dir, file)):
            continue

        shutil.copyfile(os.path.join(coin_imgs_dir, file), os.path.join(category_dir, file))

recopy('head')
recopy('tail')
recopy('other')

