"""
- https://www.pref.chiba.lg.jp/shippei/press/2019/documents/chiba_corona_data.xlsx
- PCR検査状況シート

上記を集計したものを出力

詳細なデータ
```
{
    "判明日": "1\/25\/2020",
    "陽性確認": "0 ",
    "陰性確認": "0 ",
    "合計": "3 ",
},
```

"""

from openpyxl import load_workbook
import os
import glob
from datetime import timedelta
from functools import reduce
from pathlib import Path
import sys
sys.path.append(str(Path('__file__').resolve().parent))
from common import excel_date
modified_date = None

def _empty_data(date):
    return {
        "判明日": date.strftime('%-m/%-d/%Y'),
        "陽性確認": 0,
        "陰性確認": 0,
        "合計": 0
    }

def inspections_modified():
    FILENAME = "chiba.xlsx"
    paths = [os.path.abspath(os.path.dirname(__file__)), '..', 'data', FILENAME]
    f = glob.glob(os.path.join(*paths))[0]
    wb = load_workbook(f)
    return wb.properties.modified

def _inspection_dataset_from_chiba_pref():
    FILENAME = "chiba.xlsx"
    SHEETNAME = "PCR検査状況"
    """
    検査実績（データセット）の処理
    """
    paths = [os.path.abspath(os.path.dirname(__file__)), '..', 'data', FILENAME]
    f = glob.glob(os.path.join(*paths))[0]
    data = {}
    wb = load_workbook(f)
    ws = wb[SHEETNAME]
    i = 0
    for row in ws.values:
        i += 1
        if i == 2: # modified date
            modified_date = row[4] #original data is  like "令和2年6月14日時点"
            continue
        if i in [1, 2, 3, 4]: # pass header
            continue
        if not row[1]: # pass empty row
            continue
        definite_date = row[1]
        target_date = definite_date.date()
        if not target_date in data.keys():
            data[target_date] = _empty_data(target_date)
        data[target_date]["陽性"] = row[2]
        data[target_date]["陰性"] = row[3]
        data[target_date]["合計"] = row[4]
    return data

def _fill_data(data):
    """
    空の日付にデータを埋める
    """
    from_day = min(data.keys())
    to_day = max(data.keys())
    for i in range((to_day - from_day).days + 1):
        d = from_day + timedelta(i)
        if not d in data.keys():
            data[d] = _empty_data(d)
    return data

def _data_to_inspections(data):
    """
    inspectionsのデータを作成
    """
    inspections = []
    inspections_summary_data = {
        "県内": [],
        "その他": []
    }
    inspections_summary_labels = []
    keys = sorted(data.keys())
    for key in keys:
        inspections.append(data[key])
        inspections_summary_data["県内"].append(data[key]["合計"])
        inspections_summary_data["その他"].append(int(0)) # alwasy 0
        inspections_summary_labels.append(key.strftime("%-m/%-d"))
    return inspections, inspections_summary_data, inspections_summary_labels

def _total_count(data):
    total_count = reduce(lambda x, y: x + y, [x["合計"] for x in data.values()])
    return total_count

def parse_inspection_per_date():
    data = _inspection_dataset_from_chiba_pref()
    data = _fill_data(data)
    total_count = _total_count(data)
    return  _data_to_inspections(data), total_count

if __name__ == '__main__':
    print(parse_inspection_per_date())


