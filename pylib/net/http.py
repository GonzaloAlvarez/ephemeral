#!/usr/bin/env python
import json
import tempfile
import os
import shutil

# Python 2/3 compatibility mode
try:
    from urllib.parse import urlparse
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError, URLError
except ImportError:
    from urlparse import urlparse
    from urllib2 import urlopen, Request, HTTPError, URLError

def get_json(url):
    request = Request(url)
    response = urlopen(request)
    response_data = response.read()
    encoding = response.info().get_content_charset('utf-8')
    return json.loads(response_data.decode(encoding))

def download_file(url):
    request = Request(url)
    with urlopen(request) as response, tempfile.NamedTemporaryFile('wb', delete=False) as tf:
        shutil.copyfileobj(response, tf)
        return tf.name
    
