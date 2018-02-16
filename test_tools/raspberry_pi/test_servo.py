# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO

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
        pass

    def move_to_left(self, wait=1):
        self.pwm.ChangeDutyCycle(self.left)
        time.sleep(wait)

    def move_to_middle(self, wait=1):
        self.pwm.ChangeDutyCycle(self.middle)
        time.sleep(wait)

    def move_to_right(self, wait=1):
        self.pwm.ChangeDutyCycle(self.right)
        time.sleep(wait)

class Main:

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.servo = Servo()

    def cleanup(self):
        self.servo.cleanup()
        GPIO.cleanup()

    def run(self):
        while True:
            self.servo.move_to_right(0.5)
            self.servo.move_to_left(0.5)
            self.servo.move_to_right(0.5)
            self.servo.move_to_left()
            time.sleep(3)

if __name__ == '__main__':
    main = Main()
    try:
        main.run()
    except KeyboardInterrupt:
        main.cleanup()
        print('cleanup done')
