# -*- coding: utf-8 -*-

import os
from bottle import route, run, request

####

upload_dir = 'upload_files'

####

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

    return 'success'

run(host='0.0.0.0', port=8080, debug=True, reloader=False)
