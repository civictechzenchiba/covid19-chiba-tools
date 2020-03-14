from openpyxl import load_workbook
import glob
from datetime import datetime, date, timedelta, time
import json

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

# xlsxの処理
total_count = 0
patients_count = 0
discharge_count = 0
stayed_count = 0
tiny_injury_count = 0 # 軽症
severe_injury_count = 0 # 重症
patients_summary_data = {}
for f in glob.glob('./downloads/*.xlsx'):
    wb = load_workbook(f)
    ws = wb.active
    i = 0
    for row in ws.values:
        i += 1
        if i == 1: # pass header
            continue
        total_count += 1
        update_at = datetime.strptime(str(row[0]), "%Y%m%d%H%M")
        no = row[1]
        year = row[2]
        sex = row[3]
        where_lived = row[4]
        stayed_at_wuhan = row[5]
        source = row[6] # 感染源
        category = row[7] # 区分
        date_of_occurrence = row[8] # 発症日
        definite_date = row[9] # 検査確定日
        current_status = row[10] # 現在の症状
        hospital_stay = row[11] # 入院状況
        discharge = ''
        if hospital_stay == "退院":
            discharge = '〇'
        # 陽性
        if current_status:
            patients_data = {
                "リリース日": update_at.isoformat(timespec='milliseconds')+'Z',
                "曜日": total_count,
                "居住地": where_lived,
                "年代": year,
                "性別": sex,
                "退院": discharge,
                "date": definite_date.strftime("%Y-%m-%d")
            }
            data["patients"]["data"].append(patients_data)
            target_date = definite_date.date()
            patients_count += 1
            if hospital_stay == "退院":
                discharge_count += 1
            else:
                stayed_count += 1
                if current_status == "重症":
                    severe_injury_count += 1
                else:
                    tiny_injury_count += 1
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
print(json.dumps(data))