# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO

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

class Main:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.light = Light()

    def cleanup(self):
        self.light.cleanup()
        GPIO.cleanup()

    def run(self):
        while True:
            self.light.on()
            time.sleep(3)
            self.light.off()
            time.sleep(3)

if __name__ == '__main__':
    main = Main()
    try:
        main.run()
    except KeyboardInterrupt:
        main.cleanup()
        print('cleanup done')
