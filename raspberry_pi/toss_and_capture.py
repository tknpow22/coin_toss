# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import datetime
import io
import requests
import time

import RPi.GPIO as GPIO
import picamera

# 画像のアップロード先 URL
UPLOAD_URL = 'http://192.168.1.7:8080/upload'

# 最大試行回数
TRY_COUNT = 100

# サーボ(SG90)を制御する
class Servo:

    def __init__(self):
        self.pin = 17

        self.left = 2.5
        self.middle = 7.0
        self.right = 12.0

        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(self.middle)

    def cleanup(self):
        self.pwm.stop()

    def move_to_left(self, wait=1):
        self.pwm.ChangeDutyCycle(self.left)
        time.sleep(wait)

    def move_to_middle(self, wait=1):
        self.pwm.ChangeDutyCycle(self.middle)
        time.sleep(wait)

    def move_to_right(self, wait=1):
        self.pwm.ChangeDutyCycle(self.right)
        time.sleep(wait)

# LED を制御する
class Light:

    def __init__(self):
        self.pin = 22

        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def cleanup(self):
        GPIO.output(self.pin, GPIO.LOW)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

# コイン投げを行う
class CoinToss:

    def __init__(self):
        self.servo = Servo()

    def cleanup(self):
        self.servo.cleanup()

    def toss(self):
        self.servo.move_to_right(0.5)
        self.servo.move_to_left(0.5)
        self.servo.move_to_right(0.5)
        self.servo.move_to_left()

# タクトスイッチの状態を取得する
class Button:

    def __init__(self):
        self.pin = 4

        GPIO.setup(self.pin, GPIO.IN)

    def cleanup(self):
        pass

    def is_on(self):
        return GPIO.input(self.pin) == GPIO.HIGH

# メイン処理
class Main:

    def __init__(self):

        self.args = self.parse_args()

        self.camera = picamera.PiCamera()

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.coin_toss = CoinToss()
        self.light = Light()
        self.button = Button()

    def cleanup(self):
        self.coin_toss.cleanup()
        self.light.cleanup()
        self.button.cleanup()
        GPIO.cleanup()

    def parse_args(self):
        argparser = ArgumentParser()

        argparser.add_argument('-m', '--manual',
                               action='store_true',
                               help='manual running')

        return argparser.parse_args()

    def capture(self):
        stream = io.BytesIO()
        self.camera.resolution = (150, 150)
        self.camera.capture(stream, 'jpeg')
        stream.seek(0)

        return stream

    def upload(self, stream):
        now = datetime.datetime.now()
        filename = now.strftime("%Y%m%d%H%M%S") + '.jpg'
        result = 'failure'

        try:
            response = requests.post(UPLOAD_URL, files={'picture': (filename, stream, 'image/jpeg')}, data={'uploadfrom': 'coin_capture'})
            result = response.text
        except Exception as ex:
            print(ex.args)

        print('upload(): [%s]: [%s]' % (result, filename))

    def run_manual(self):
        while True:
            if self.button.is_on():
                self.coin_toss.toss()

                time.sleep(1)

                self.light.on()

                with self.capture() as stream:
                    self.upload(stream)

                self.light.off()

            time.sleep(1)

    def run_auto(self):
        for _ in range(0, TRY_COUNT):
            self.coin_toss.toss()

            time.sleep(1)

            self.light.on()

            with self.capture() as stream:
                self.upload(stream)

            self.light.off()

            time.sleep(7)

    def run(self):
        if self.args.manual:
            self.run_manual()
        else:
            self.run_auto()

if __name__ == '__main__':
    main = Main()
    try:
        main.run()
    except KeyboardInterrupt:
        pass
    finally:
        main.cleanup()
        print('cleanup done')
