from openpyxl import load_workbook
import glob
from datetime import datetime

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
for f in glob.glob('./downloads/*.xlsx'):
    wb = load_workbook(f)
    ws = wb.active
    i = 0
    for row in ws.values:
        i = i + 1
        if i == 1:
            continue
        total_count = total_count + 1
        update_at = datetime.strptime(str(row[0]), "%Y%m%d%H%M")
        no = row[1]
        year = row[2]
        sex = row[3]
        where_lived = row[4]
        stayed_at_wuhan = row[5]
        source = row[6] # 感染源
        category = row[7] # 区分
        date_of_occurrence = row[8] # 発症日
        if date_of_occurrence:
            date_of_occurrence = date_of_occurrence.strftime("%Y-%m-%d")
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
                "date": date_of_occurrence
            }
            data["patients"]["data"].append(patients_data)
            patients_count = patients_count + 1
            if hospital_stay == "退院":
                discharge_count = discharge_count + 1
            else:
                stayed_count = stayed_count + 1
                if current_status == "重症":
                    severe_injury_count = severe_injury_count + 1
                else:
                    tiny_injury_count = tiny_injury_count + 1
                    
# カウントをいれる
data["main_summary"]["value"] = total_count
data["main_summary"]["children"][0]["value"] = patients_count
data["main_summary"]["children"][0]["children"][0]["value"] = stayed_count
data["main_summary"]["children"][0]["children"][1]["value"] = discharge_count
data["main_summary"]["children"][0]["children"][0]["children"][0]["value"] = tiny_injury_count
data["main_summary"]["children"][0]["children"][0]["children"][1]["value"] = severe_injury_count
