"""
【<日付>】千葉県_感染者発生状況.xlsxの処理
"""

from openpyxl import load_workbook
import os
import glob
from pathlib import Path
import sys
sys.path.append(str(Path('__file__').resolve().parent))
from common import excel_date

def parse_chiba_patients_list():
    FILENAME = "【*】千葉県_感染者発生状況.xlsx"
    paths = [os.path.abspath(os.path.dirname(__file__)), '..', 'data', FILENAME]
    patients_count = 0 # 陽性患者数
    discharge_count = 0 # 退院
    stayed_count = 0 # 入院
    tiny_injury_count = 0 # 軽症
    severe_injury_count = 0 # 重症
    data = {} # 千葉県専用のグラフ用のデータ
    patients_list = [] # 患者の表の表示用
    # 健康福祉部のデータ処理
    f = glob.glob(os.path.join(*paths))[0]
    wb = load_workbook(f)
    ws = wb.active
    inloop = False
    target = None
    for row in ws.values:
        if '患者' in str(row[0]):
            target = "patient"
        elif '無症状病原体保有者' in str(row[0]):
            target = "no_symptom"
        if row[1]:
            inloop = True
            if 'No' in str(row[1]):
                continue
        else:
            inloop = False
        if not inloop:
            continue
        no = row[1] # No.
        year = row[2] # 年代
        sex = row[3] # 性別
        where_lived = row[4] # 居住地
        category = row[5] # 区分
        if isinstance(row[6], int):
            date_of_occurrence = excel_date(row[6]) # 発症日
        else:
            date_of_occurrence = ''
        definite_date = excel_date(row[7]) # 検査確定日
        current_status = row[8] # 直近の症状
        hospital_stay = row[9] # 入院状況
        discharge = ''
        if hospital_stay == "退院": # TODO 自宅待機をどう扱うか
            discharge = '〇'
        # 陽性陰性両方ともグラフに表示する
        target_date = definite_date.date()
        if not target_date in data:
            data[target_date] = {
                "patients": 0,
                "no_symptoms": 0,
                "labels": target_date.strftime("%-m/%-d"),
                "day": target_date
            }
        # 患者
        if target == "patient":
            patients_data = {
                "リリース日": definite_date.isoformat(timespec='milliseconds')+'Z', # 公表日はなくなった
                "曜日": '',
                "居住地": where_lived,
                "年代": year,
                "性別": sex,
                "退院": discharge,
                "date": definite_date.strftime("%Y-%m-%d")
            }
            patients_list.append(patients_data)
            
            patients_count += 1
            if hospital_stay == "退院":
                discharge_count += 1
            else:
                stayed_count += 1
                if current_status == "重症":
                    severe_injury_count += 1
                else:
                    tiny_injury_count += 1
            data[target_date]["patients"] += 1
        # 無感染
        else:
            data[target_date]["no_symptoms"] += 1
    return patients_count, discharge_count, stayed_count, tiny_injury_count, severe_injury_count, data, patients_list
