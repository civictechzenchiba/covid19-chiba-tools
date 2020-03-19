from openpyxl import load_workbook
import glob
from datetime import datetime, date, time, timedelta
import json
from common import excel_date

from processing.inspection_summary import parse_inspection_summary
from processing.call_center import parse_call_center
from processing.inspection_per_date import parse_inspection_per_date
from processing.querents import parse_querents
from processing.patients import parse_chiba_patients_list

(inspections, inspections_summary_data, inspections_summary_labels), total_count = parse_inspection_per_date()
patients_count, discharge_count, stayed_count, tiny_injury_count, severe_injury_count, patients_and_no_symptoms_summary_data, patients_list = parse_chiba_patients_list()

# patients_and_no_symptoms_summary_dataに0件のデータを入れる
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
patients_and_no_symptoms_summary_data_patients = []
patients_and_no_symptoms_summary_data_no_symptoms = []
patients_and_no_symptoms_summary_labels = []
for d in sorted_values:
    patients_and_no_symptoms_summary_data_patients.append(d["patients"])
    patients_and_no_symptoms_summary_data_no_symptoms.append(d["no_symptoms"])
    patients_and_no_symptoms_summary_labels.append(d["labels"])

# data.json 雛形
data = {
    # コールセンター相談件数
    "contacts": { 
        "date": datetime.now().strftime('%Y/%m/%d %H:%M'),
        "data": parse_call_center()
    },
    # 帰国者接触者センター相談件数
    "querents": {
        "date": datetime.now().strftime('%Y/%m/%d %H:%M'),
        "data": parse_querents()
    },
    # 陽性患者
    "patients": {
        "date": datetime.now().strftime('%Y/%m/%d %H:%M'),
        "data": patients_list
    },
    "patients_summary": {
        "date": datetime.now().strftime('%Y/%m/%d %H:%M'),
        "data": []
    },
    # 千葉県用データ: 患者と非患者のサマリ
    "patients_and_no_symptoms_summary": {
        "date": datetime.now().strftime('%Y/%m/%d %H:%M'),
        "data": {
            "患者": patients_and_no_symptoms_summary_data_patients,
            "無症状病原体保有者": patients_and_no_symptoms_summary_data_no_symptoms
        },
        "labels": patients_and_no_symptoms_summary_labels
    },
    # 退院者
    "discharges_summary": {
        "date": datetime.now().strftime('%Y/%m/%d %H:%M'),
        "data": []
    },
    "discharges": {
        "date": datetime.now().strftime('%Y/%m/%d %H:%M'),
        "data": []
    },
    # 検査実施数
    "inspections": {
        "date": datetime.now().strftime('%Y/%m/%d %H:%M'),
        "data": inspections
    },
    "inspections_summary": {
        "date": datetime.now().strftime('%Y/%m/%d %H:%M'),
        "data": inspections_summary_data,
        "labels": inspections_summary_labels
    },
    # 未使用？
    "better_patients_summary": {
        "date": datetime.now().strftime('%Y/%m/%d %H:%M'),
        "data": []
    },
    "lastUpdate": datetime.now().strftime('%Y/%m/%d %H:%M'),
    "main_summary": {
        "attr": "検査実施人数",
        "value": total_count,
        "children": [
            {
                "attr": "陽性患者数",
                "value": patients_count,
                "children": [
                    {
                        "attr": "入院中",
                        "value": stayed_count,
                        "children": [
                            {
                                "attr": "軽症・中等症",
                                "value": tiny_injury_count
                            },
                            {
                                "attr": "重症",
                                "value": severe_injury_count
                            }
                        ]
                    },
                    {
                        "attr": "退院",
                        "value": discharge_count
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

print(json.dumps(data))