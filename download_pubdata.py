#!/usr/bin/env python

import shutil
import urllib.request
import os
import ssl
from datetime import date
from datetime import timedelta
from urllib.request import Request, urlopen
from urllib.error import URLError

# ssl設定
context = ssl._create_unverified_context()


def _openurl(someurl):
    req = Request(someurl)
    try:
        urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason, someurl)
            return -1
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code, someurl)
            return e.code
    else:
        print("download success:" + someurl)
        return 1


def download(isLocal=True):
    base = "https://www.pref.chiba.lg.jp/shippei/press/2019/documents/"
    defaultfile = "chiba_corona_data.xlsx"
    filename = "chiba.xlsx"
    if isLocal:
        output = os.path.join(*[os.path.abspath(os.path.dirname(__file__)), 'data', filename])
    else:
        output = os.path.join('/tmp', filename)
    # 2020 12/17 以降 日付が先頭にのこるようになった問題の対応
    todaystr = date.today().strftime("%m%d")
    yesterdaystr = (date.today() - timedelta(days=1)).strftime("%m%d")
    print(todaystr, yesterdaystr)
    if 1 == _openurl(base + todaystr + defaultfile):
        targeturl = base + todaystr + defaultfile
        print("url is today")
    elif 1 == _openurl(base + yesterdaystr + defaultfile):
        targeturl = base + yesterdaystr + defaultfile
    else:
        targeturl = base + defaultfile
        print("use default")

    with urllib.request.urlopen(targeturl, context=context) as response:
        with open(output, 'wb') as fp:
            shutil.copyfileobj(response, fp)


if __name__ == '__main__':
    download()
