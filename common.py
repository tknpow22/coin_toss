# -*- coding: utf-8 -*-

import math
import cv2
import numpy as np
from keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPooling2D
from keras.models import Sequential

class Common:
    COLORS = 3

    UPLOAD_IMG_WIDTH = 50
    UPLOAD_IMG_HEIGHT = 50

    IMG_WIDTH = 50
    IMG_HEIGHT = 50

    INPUT_SHAPE = (IMG_HEIGHT, IMG_WIDTH, COLORS)

    CLASSES = ('head', 'tail', 'other')
    NUM_CLASSES = len(CLASSES)

class CoinImage:
    # 入力画像内の硬貨の半径の最小値
    # - 硬貨(円)を検出する際に使用
    # - MIN_COIN_R < MAX_COIN_R となること
    MIN_COIN_R = 15

    # 入力画像内の硬貨の半径の最大値
    # - 硬貨(円)を検出する際に使用
    # - 倍にした値を出力画像のサイズとして使用
    # - MIN_COIN_R < MAX_COIN_R となること
    MAX_COIN_R = 25

    # 出力画像のサイズ
    # - MAX_COIN_R <= OUTPUT_IMG_R となること
    OUTPUT_IMG_R = MAX_COIN_R
    OUTPUT_IMG_SIZE = OUTPUT_IMG_R * 2

    # 円の外側部分を作る際に、色をサンプリングする座標値

    __degree = 45
    __radian = math.radians(__degree)
    __point = int(math.sin(__radian) * OUTPUT_IMG_R)

    CI_X_TOP_LEFT = OUTPUT_IMG_R - __point
    CI_Y_TOP_LEFT = OUTPUT_IMG_R - __point

    CI_X_TOP_RIGHT = OUTPUT_IMG_R + __point
    CI_Y_TOP_RIGHT = OUTPUT_IMG_R - __point

    CI_X_BOTTOM_LEFT = OUTPUT_IMG_R - __point
    CI_Y_BOTTOM_LEFT = OUTPUT_IMG_R + __point

    CI_X_BOTTOM_RIGHT = OUTPUT_IMG_R + __point
    CI_Y_BOTTOM_RIGHT = OUTPUT_IMG_R + __point

    @staticmethod
    def scale(x):
        x = x + max(-np.min(x), 0)
        x_max = np.max(x)
        if x_max != 0:
            x /= x_max
        x *= 255
        return x

    @staticmethod
    def get_img(img_file_path):
        # RGB 画像として読み込む
        # (h, w, c), c:(b,g,r), c: 0 - 255
        img = cv2.imread(img_file_path)
        if img is None:
            return None

        # グレースケールに変換する
        gimg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # 画像を平滑化する（ぼかす）
        bimg = cv2.medianBlur(gimg, 5)

        # 円(硬貨とおぼしき領域)を検出する
        circles = cv2.HoughCircles(bimg, cv2.HOUGH_GRADIENT,
                        1, 30,
                        #param1=5, param2=30,
                        param1=5, param2=15,
                        minRadius=CoinImage.MIN_COIN_R, maxRadius=CoinImage.MAX_COIN_R)

        if circles is not None:
            # 座標値を四捨五入する
            circles = np.uint16(np.around(circles))

            for c in circles[0,:]:
                # 円の中心座標と半径を得る
                center_x = int(c[0])
                center_y = int(c[1])
                r = int(c[2])

                # 円を囲む矩形の左上座標を得る
                top = max(center_y - r, 0)
                left = max(center_x - r, 0)

                # 矩形の左上座標のカラー値を得る
                dot_top_left = img[top, left]
                #dot_top_right = img[top, left+(r*2)-1]
                #dot_bottom_left = img[top+(r*2)-1, left]
                #dot_bottom_right = img[top+(r*2)-1, left+(r*2)-1]

                # 出力画像のサイズにあわせて取得する円を囲む矩形領域を決める
                src_top = max(center_y - CoinImage.OUTPUT_IMG_R, 0)
                src_bottom = min(src_top + CoinImage.OUTPUT_IMG_SIZE, img.shape[0])
                src_left = max(center_x - CoinImage.OUTPUT_IMG_R, 0)
                src_right = min(src_left + CoinImage.OUTPUT_IMG_SIZE, img.shape[1])

                height = src_bottom - src_top
                width = src_right - src_left

                dest_top = (CoinImage.OUTPUT_IMG_SIZE - height) // 2
                dest_left = (CoinImage.OUTPUT_IMG_SIZE - width) // 2

                # 出力画像を作成
                aimg = np.zeros((CoinImage.OUTPUT_IMG_SIZE, CoinImage.OUTPUT_IMG_SIZE, Common.COLORS), np.uint8)

                # 念のため、出力画像を円を囲む矩形の左上座標のカラー値で埋めておく
                aimg[0:CoinImage.OUTPUT_IMG_SIZE, 0:CoinImage.OUTPUT_IMG_SIZE] = dot_top_left

                # 出力画像に円内の画像をコピーする
                aimg[dest_top:dest_top+height, dest_left:dest_left+width] = img[src_top:src_bottom, src_left:src_right]

                # 円の外側部分を作るためのカラー値を得る
                ci_dot_top_left = aimg[CoinImage.CI_Y_TOP_LEFT, CoinImage.CI_X_TOP_LEFT]
                ci_dot_top_right = aimg[CoinImage.CI_Y_TOP_RIGHT, CoinImage.CI_X_TOP_RIGHT]
                ci_dot_bottom_left = aimg[CoinImage.CI_Y_BOTTOM_LEFT, CoinImage.CI_X_BOTTOM_LEFT]
                ci_dot_bottom_right = aimg[CoinImage.CI_Y_BOTTOM_RIGHT, CoinImage.CI_X_BOTTOM_RIGHT]

                # 円部分のみ取り出す
                mimg1 = np.zeros((CoinImage.OUTPUT_IMG_SIZE, CoinImage.OUTPUT_IMG_SIZE, Common.COLORS), np.uint8)
                cv2.circle(mimg1, (CoinImage.OUTPUT_IMG_R,CoinImage.OUTPUT_IMG_R), CoinImage.OUTPUT_IMG_R, (1,1,1), -1)
                timg1 = aimg * mimg1

                ##### 円の外側部分を作る
                ####mimg2 = np.ones((CoinImage.OUTPUT_IMG_SIZE, CoinImage.OUTPUT_IMG_SIZE, Common.COLORS), np.uint8)
                ####cv2.circle(mimg2, (CoinImage.OUTPUT_IMG_R,CoinImage.OUTPUT_IMG_R), CoinImage.OUTPUT_IMG_R, (0,0,0), -1)
                ####timg2 = mimg2

                # 円の外側部分を作る(グラデーションさせる)
                bkimg = np.zeros((CoinImage.OUTPUT_IMG_SIZE, CoinImage.OUTPUT_IMG_SIZE, Common.COLORS), np.uint8)

                # b, g, r
                ####b1, g1, r1 = dot_top_left.astype(np.float)
                ####b2, g2, r2 = dot_top_right.astype(np.float)
                ####b3, g3, r3 = dot_bottom_left.astype(np.float)
                ####b4, g4, r4 = dot_bottom_right.astype(np.float)
                b1, g1, r1 = ci_dot_top_left.astype(np.float)
                b2, g2, r2 = ci_dot_top_right.astype(np.float)
                b3, g3, r3 = ci_dot_bottom_left.astype(np.float)
                b4, g4, r4 = ci_dot_bottom_right.astype(np.float)

                for y in range(0, CoinImage.OUTPUT_IMG_SIZE):
                    for x in range(0, CoinImage.OUTPUT_IMG_SIZE):
                        ra = x / (CoinImage.OUTPUT_IMG_SIZE-1)
                        rb = y / (CoinImage.OUTPUT_IMG_SIZE-1)


                        b = ra * rb * (b1 - b2 - b3 + b4) - ra * (b1 - b2) - rb * (b1 - b3) + b1
                        g = ra * rb * (g1 - g2 - g3 + g4) - ra * (g1 - g2) - rb * (g1 - g3) + g1
                        r = ra * rb * (r1 - r2 - r3 + r4) - ra * (r1 - r2) - rb * (r1 - r3) + r1

                        bkimg[y, x] = np.array([b, g, r]).astype(np.uint8)

                mimg2 = np.ones((CoinImage.OUTPUT_IMG_SIZE, CoinImage.OUTPUT_IMG_SIZE, Common.COLORS), np.uint8)
                cv2.circle(mimg2, (CoinImage.OUTPUT_IMG_R,CoinImage.OUTPUT_IMG_R), CoinImage.OUTPUT_IMG_R, (0,0,0), -1)

                timg2 = bkimg * mimg2


                # 円部分と円の外側部分を合成する
                rimg = timg1 ^ timg2

                result = (rimg - np.mean(rimg)) / np.std(rimg) * 16 + 64

                # Keras 2.1.2 の ImageDataGenerator.flow_from_directory() で生成される画像が
                # scale された状態で取得されるため、
                # Model.fit_generator() 時と Model.predict() 時に同じようになるよう、
                # あらかじめ scale しておく
                result = CoinImage.scale(result)

                # 最初のひとつだけを返す
                # (h, w, c), c:(b,g,r), c: 0 - 255
                return result

        return None

class MyModel:

    @staticmethod
    def get_model():
        # https://github.com/keras-team/keras/blob/master/examples/mnist_cnn.py
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3),
                         activation='relu',
                         input_shape=Common.INPUT_SHAPE))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(Common.NUM_CLASSES, activation='softmax'))

        return model

