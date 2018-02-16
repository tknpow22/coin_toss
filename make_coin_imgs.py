# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import os
import cv2
from common import CoinImage

####

def parse_args():
    argparser = ArgumentParser()

    argparser.add_argument('-t', '--test',
                           action='store_true',
                           help='test running')

    return argparser.parse_args()

####

args = parse_args()

orig_imgs_dir = 'orig_imgs'
coin_imgs_dir = 'coin_imgs'

if args.test:
    orig_imgs_dir = 'test_orig_imgs'
    coin_imgs_dir = 'test_coin_imgs'

os.makedirs(coin_imgs_dir, exist_ok=True)

files = os.listdir(orig_imgs_dir)
for file in files:
    if file.endswith('jpg') or file.endswith('jpeg'):
        img = CoinImage.get_img(os.path.join(orig_imgs_dir, file))
        if img is not None:
            cv2.imwrite(os.path.join(coin_imgs_dir, file), img)
        else:
            print('no coin image:', file)
