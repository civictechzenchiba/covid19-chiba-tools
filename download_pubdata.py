#!/usr/bin/env python

import shutil
import urllib.request
import csv
import tempfile
import os
import glob
import ssl

# ssl設定
context = ssl._create_unverified_context()

def download(isLocal=True):
    url="https://www.pref.chiba.lg.jp/shippei/press/2019/documents/chiba_corona_data.xlsx"
    filename = "chiba.xlsx"
    if isLocal:
        output = os.path.join(*[os.path.abspath(os.path.dirname(__file__)), 'data', filename])
    else:
        output = os.path.join('/tmp', filename)
    with urllib.request.urlopen(url, context=context) as response:
        with open(output, 'wb') as fp:
            shutil.copyfileobj(response, fp)
    

if __name__ == '__main__':
    download()