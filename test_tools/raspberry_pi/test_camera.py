# -*- coding: utf-8 -*-

import datetime
import io
import requests
import picamera
import time

# 画像のアップロード先 URL
UPLOAD_URL = 'http://192.168.1.7:8080/upload'

class Main:

    def __init__(self):
        self.camera = picamera.PiCamera()

    def cleanup(self):
        pass

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

    def run(self):
        while True:
            with self.capture() as stream:
                self.upload(stream)

            time.sleep(5)

if __name__ == '__main__':
    main = Main()
    try:
        main.run()
    except KeyboardInterrupt:
        main.cleanup()
        print('cleanup done')
