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
    ENTRY_POINT="https://docs.google.com/spreadsheets/d/1v24qeS70ZwVtvvDBnMgGviW83O_O9-LFGi8-jLxXI9U/export?format=tsv&gid=0"
    
    # 【<日付>】千葉県_感染者発生状況.xlsx
    patients_filename = ""
    patients_url = ""

    # 検査実績（データセット）千葉県衛生研究所2019-nCoVラインリスト<日付>.xlsx
    inspection_per_date_chiba_pref_filename = ""
    inspection_per_date_chiba_pref_url = ""

    # 千葉市検査実施日状況
    inspection_per_date_chiba_city_filename = "検査実施日別状況.xlsx"
    inspection_per_date_chiba_city_url = ""

    # 検査実施サマリ.xlsx
    inspection_summary_filename = "検査実施サマリ.xlsx"
    inspection_summary_url = ""

    # 千葉市帰国者接触者センター相談件数-RAW
    querents_filename = "帰国者接触者センター相談件数-RAW.xlsx"
    querents_url = ""

    # 千葉市コールセンター相談件数-RAWファイルURL
    call_center_filename = "コールセンター相談件数-RAW.xlsx"
    call_center_url = ""

    with urllib.request.urlopen(ENTRY_POINT, context=context) as response:
        body = response.read().decode('UTF-8')
        r = csv.reader(body.strip().splitlines(), delimiter = '\t')
        for row in r:
            if len(row) < 2:
                continue
            if row[2] != '':
                patients_filename = row[1]
                patients_url = row[2]
            if len(row) < 4:
                continue
            if row[4] != '':
                inspection_per_date_chiba_pref_filename = row[3]
                inspection_per_date_chiba_pref_url = row[4]
            if len(row) < 6:
                continue
            if row[6] != '':
                inspection_per_date_chiba_city_url = row[6]
            if len(row) < 8:
                continue
            if row[8] != '':
                inspection_summary_url = row[8]
            if len(row) < 10:
                continue
            if row[10] != '':
                querents_url = row[10]
            if len(row) < 12:
                continue
            if row[12] != '':
                call_center_url = row[12]
    _delete_data_directory_files()
    _download_each_file(patients_filename, patients_url)
    _download_each_file(inspection_per_date_chiba_pref_filename, inspection_per_date_chiba_pref_url)
    _download_each_file(inspection_per_date_chiba_city_filename, inspection_per_date_chiba_city_url)
    _download_each_file(inspection_summary_filename, inspection_summary_url)
    _download_each_file(querents_filename, querents_url)
    _download_each_file(call_center_filename, call_center_url)

def _delete_data_directory_files():
    targets = os.path.join(*[os.path.abspath(os.path.dirname(__file__)), 'data', "*.xlsx"])
    files = glob.glob(targets)
    for f in files:
        os.remove(f)

def _download_each_file(filename, url):
    url = url.replace('https://drive.google.com/open?id=', 'https://drive.google.com/uc?export=download&id=')
    print(url)
    print(filename)
    output = os.path.join(*[os.path.abspath(os.path.dirname(__file__)), 'data', filename])
    with urllib.request.urlopen(url, context=context) as response:
        with open(output, 'wb') as fp:
            shutil.copyfileobj(response, fp)

if __name__ == '__main__':
    download()