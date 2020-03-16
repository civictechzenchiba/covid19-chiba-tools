from openpyxl import load_workbook
import glob
from datetime import datetime, date, timedelta, time
import json

def excel_date(num):
    return (datetime(1899, 12, 30) + timedelta(days=num))

# data.json 雛形
data = {
    # 
    "contacts": { 
        "date": '',
        "data": []
    },
    "querents": {
        "date": '',
        "data": []
    },
    # 陽性患者
    "patients": {
        "date": '',
        "data": []
    },
    "patients_summary": {
        "date": '',
        "data": []
    },
    # 千葉県用データ: 患者と非患者のサマリ
    "patients_and_no_symptoms_summary": {
        "date": "",
        "data": {
            "患者": [],
            "無症状病原体保有者": []
        },
        "labels": []
    },
    # 退院者
    "discharges_summary": {
        "date": '',
        "data": []
    },
    "discharges": {
        "date": '',
        "data": []
    },
    # 検査実施数
    "inspections": {
        "date": '',
        "data": []
    },
    "inspections_summary": {
        "date": '',
        "data": []
    },
    # 未使用？
    "better_patients_summary": {
        "date": '',
        "data": []
    },
    "lastUpdate": '',
    "main_summary": {
        "attr": "検査実施人数",
        "value": 0,
        "children": [
            {
                "attr": "陽性患者数",
                "value": 0,
                "children": [
                    {
                        "attr": "入院中",
                        "value": 0,
                        "children": [
                            {
                                "attr": "軽症・中等症",
                                "value": 0
                            },
                            {
                                "attr": "重症",
                                "value": 0
                            }
                        ]
                    },
                    {
                        "attr": "退院",
                        "value": 0
                    },
                    {
                        "attr": "死亡",
                        "value": 0
                    }
                ]
            }
        ]
    }
}

# 合計数の初期化
total_count = 0
patients_count = 0
discharge_count = 0
stayed_count = 0
tiny_injury_count = 0 # 軽症
severe_injury_count = 0 # 重症
patients_and_no_symptoms_summary_data = {} # 千葉県用のサマリ
# 健康福祉部のデータ処理
for f in glob.glob('./health_and_welfare_department/*.xlsx'):
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
        total_count += 1
        no = row[1]
        year = row[2]
        sex = row[3]
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
        if hospital_stay == "退院":
            discharge = '〇'
        # 陽性陰性両方ともグラフに表示する
        target_date = definite_date.date()
        if not target_date in patients_and_no_symptoms_summary_data:
            patients_and_no_symptoms_summary_data[target_date] = {
                "patients": 0,
                "no_symptoms": 0,
                "labels": target_date.strftime("%-m/%-d"),
                "day": target_date
            }
        total_count += 1
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
            data["patients"]["data"].append(patients_data)
            
            patients_count += 1
            if hospital_stay == "退院":
                discharge_count += 1
            else:
                stayed_count += 1
                if current_status == "重症":
                    severe_injury_count += 1
                else:
                    tiny_injury_count += 1
            patients_and_no_symptoms_summary_data[target_date]["patients"] += 1
        # 無感染
        else:
            patients_and_no_symptoms_summary_data[target_date]["no_symptoms"] += 1


# 検査実績（データセット）の処理
patients_summary_data = {}
for f in glob.glob('./result_set/*.xlsx'):
    wb = load_workbook(f)
    ws = wb.active
    i = 0
    for row in ws.values:
        i += 1
        if i == 1: # pass header
            continue
        if not row[0]: # pass empty row
            continue
        if not row[10] == "陽性":
            continue
        definite_date = row[8]
        target_date = definite_date.date()
        if target_date in patients_summary_data:
            patients_summary_data[target_date] += 1
        else:
            patients_summary_data[target_date] = 1

# カウントをいれる
data["main_summary"]["value"] = total_count
data["main_summary"]["children"][0]["value"] = patients_count
data["main_summary"]["children"][0]["children"][0]["value"] = stayed_count
data["main_summary"]["children"][0]["children"][1]["value"] = discharge_count
data["main_summary"]["children"][0]["children"][0]["children"][0]["value"] = tiny_injury_count
data["main_summary"]["children"][0]["children"][0]["children"][1]["value"] = severe_injury_count

# patients_summary_dataに0件のデータを入れる
from_day = min(patients_summary_data.keys())
to_day = max(patients_summary_data.keys())
for i in range((to_day - from_day).days + 1):
    d = from_day + timedelta(i)
    if not d in patients_summary_data:
        patients_summary_data[d] = 0

# patients_summary を入れる
patients_summaries = []
for target_date in patients_summary_data.keys():
    patients_summaries.append({
        "日付": datetime.combine(target_date, time()).isoformat(timespec='milliseconds')+'Z',
        "小計": patients_summary_data[target_date]
    })
data["patients_summary"]["data"] = sorted(patients_summaries, key=lambda d: d["日付"])

# patients_summary_dataに0件のデータを入れる
from_day = min(patients_and_no_symptoms_summary_data.keys())
to_day = max(patients_and_no_symptoms_summary_data.keys())
for i in range((to_day - from_day).days + 1):
    d = from_day + timedelta(i)
    if not d in patients_and_no_symptoms_summary_data.keys():
        patients_and_no_symptoms_summary_data[d] = {
            "patients": 0,
            "no_symptoms": 0,
            "labels": d.strftime("%-m/%-d"),
            "day": d
        }

sorted_values = sorted(patients_and_no_symptoms_summary_data.values(), key=lambda d: d["day"])
for d in sorted_values:
    data["patients_and_no_symptoms_summary"]["data"]["患者"].append(d["patients"])
    data["patients_and_no_symptoms_summary"]["data"]["無症状病原体保有者"].append(d["no_symptoms"])
    data["patients_and_no_symptoms_summary"]["labels"].append(d["labels"])
print(json.dumps(data))