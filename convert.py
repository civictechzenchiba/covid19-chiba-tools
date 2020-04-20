from openpyxl import load_workbook
import glob
from datetime import datetime, date, time, timedelta, timezone
import json
from common import excel_date

from processing.inspection_summary import parse_inspection_summary, inspections_summary_modified
from processing.call_center import parse_call_center, call_center_modified
from processing.inspection_per_date import parse_inspection_per_date, inspections_modified
from processing.querents import parse_querents, querents_modified
from processing.patients import parse_chiba_patients_list, patients_modified

(inspections, inspections_summary_data, inspections_summary_labels), total_count = parse_inspection_per_date()
patients_count, discharge_count, stayed_count, tiny_injury_count, severe_injury_count, death_count, patients_and_no_symptoms_summary_data, patients_list = parse_chiba_patients_list()

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

contacts_date = call_center_modified()\
    .replace(tzinfo=timezone(timedelta(hours=9))) + timedelta(hours = +9)
querents_date = querents_modified()\
    .replace(tzinfo=timezone(timedelta(hours=9))) + timedelta(hours = +9)
patients_date = patients_modified()\
    .replace(tzinfo=timezone(timedelta(hours=9))) + timedelta(hours = +9)
inspections_date = inspections_modified()\
    .replace(tzinfo=timezone(timedelta(hours=9))) + timedelta(hours = +9)
inspections_summary_date = inspections_summary_modified()\
    .replace(tzinfo=timezone(timedelta(hours=9))) + timedelta(hours = +9)

contacts_date_str = contacts_date.strftime("%Y/%m/%d %H:%M")
querents_date_str = querents_date.strftime("%Y/%m/%d %H:%M")
patients_date_str = patients_date.strftime("%Y/%m/%d %H:%M")
inspections_date_str = inspections_date.strftime("%Y/%m/%d %H:%M")
inspections_summary_date_str = \
    inspections_summary_date.strftime("%Y/%m/%d %H:%M")

last_date = contacts_date
if last_date < querents_date:
    last_date = querents_date
if last_date < patients_date:
    last_date = patients_date
if last_date < inspections_date:
    last_date = inspections_date
if last_date < inspections_summary_date:
    last_date = inspections_summary_date
last_date_str = last_date.strftime("%Y/%m/%d %H:%M")

# data.json 雛形
data = {
    # コールセンター相談件数
    "contacts": { 
        "date": contacts_date_str,
        "data": parse_call_center()
    },
    # 帰国者接触者センター相談件数
    "querents": {
        "date": querents_date_str,
        "data": parse_querents()
    },
    # 陽性患者
    "patients": {
        "date": patients_date_str,
        "data": patients_list
    },
    "patients_summary": {
        "date": patients_date_str,
        "data": []
    },
    # 千葉県用データ: 患者と非患者のサマリ
    "patients_and_no_symptoms_summary": {
        "date": patients_date_str,
        "data": {
            "患者": patients_and_no_symptoms_summary_data_patients,
            "無症状病原体保有者": patients_and_no_symptoms_summary_data_no_symptoms
        },
        "labels": patients_and_no_symptoms_summary_labels
    },
    # 退院者
    "discharges_summary": {
        "date": patients_date_str,
        "data": []
    },
    "discharges": {
        "date": patients_date_str,
        "data": []
    },
    # 検査実施数
    "inspections": {
        "date": inspections_date_str,
        "data": inspections
    },
    "inspections_summary": {
        "date": inspections_date_str, # 検査実施数のデータから生成しているらしい
        "data": inspections_summary_data,
        "labels": inspections_summary_labels
    },
    # 未使用？
    "better_patients_summary": {
        "date": last_date_str,
        "data": []
    },
    "lastUpdate": last_date_str,
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
                        "value": death_count
                    }
                ]
            }
        ]
    }
}

print(json.dumps(data))
