from openpyxl import load_workbook
import glob
from datetime import datetime, date, time, timedelta, timezone
import json
from common import excel_date

from processing.inspection_per_date_pubdata import parse_inspection_per_date, inspections_modified
#from processing.querents import parse_querents, querents_modified
#from processing.patients import parse_chiba_patients_list, patients_modified

(inspections, inspections_summary_data, inspections_summary_labels), total_count = parse_inspection_per_date()
#patients_count, discharge_count, stayed_count, tiny_injury_count, severe_injury_count, death_count, patients_and_no_symptoms_summary_data, patients_list = parse_chiba_patients_list()

# patients_and_no_symptoms_summary_dataに0件のデータを入れる
'''
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
'''

inspections_date = inspections_modified()\
    .replace(tzinfo=timezone(timedelta(hours=9))) + timedelta(hours = +9)
'''
inspections_summary_date = inspections_summary_modified()\
    .replace(tzinfo=timezone(timedelta(hours=9))) + timedelta(hours = +9)

contacts_date_str = contacts_date.strftime("%Y/%m/%d %H:%M")
querents_date_str = querents_date.strftime("%Y/%m/%d %H:%M")
patients_date_str = patients_date.strftime("%Y/%m/%d %H:%M")
inspections_summary_date_str = \
    inspections_summary_date.strftime("%Y/%m/%d %H:%M")
'''
inspections_date_str = inspections_date.strftime("%Y/%m/%d %H:%M")

last_date = inspections_date
last_date_str = last_date.strftime("%Y/%m/%d %H:%M")

# data.json 雛形
data = {
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
}

print(json.dumps(data))
