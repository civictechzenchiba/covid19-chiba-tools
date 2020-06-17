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

def download():
    url="https://www.pref.chiba.lg.jp/shippei/press/2019/documents/chiba_corona_data_1.xlsx"
    filename = "chiba.xlsx"
    output = os.path.join(*[os.path.abspath(os.path.dirname(__file__)), 'data', filename])
    with urllib.request.urlopen(url, context=context) as response:
        with open(output, 'wb') as fp:
            shutil.copyfileobj(response, fp)
    

def _delete_data_directory_files():
    targets = os.path.join(*[os.path.abspath(os.path.dirname(__file__)), 'data', "*.xlsx"])
    files = glob.glob(targets)
    for f in files:
        os.remove(f)

def _download_each_file(filename, url):
    url = url.replace('https://drive.google.com/open?id=', 'https://drive.google.com/uc?export=download&id=')
    output = os.path.join(*[os.path.abspath(os.path.dirname(__file__)), 'data', filename])
    with urllib.request.urlopen(url, context=context) as response:
        with open(output, 'wb') as fp:
            shutil.copyfileobj(response, fp)

if __name__ == '__main__':
    download()