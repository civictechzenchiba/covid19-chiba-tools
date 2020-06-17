import json
from datetime import timedelta, timezone
from processing.inspection_per_date_pubdata import parse_inspection_per_date, inspections_modified
from processing.patients_pubdata import parse_patients_per_date, patients_modified

(inspections, inspections_summary_data, inspections_summary_labels), total_count = parse_inspection_per_date()
(patients, patients_summary_data, patients_summary_labels), total_conf_count, total_pub_count = parse_patients_per_date()

inspections_date = inspections_modified()\
    .replace(tzinfo=timezone(timedelta(hours=9))) + timedelta(hours=+9)
inspections_date_str = inspections_date.strftime("%Y/%m/%d %H:%M")

patients_date = patients_modified()\
    .replace(tzinfo=timezone(timedelta(hours=9))) + timedelta(hours=+9)
patients_date_str = patients_date.strftime("%Y/%m/%d %H:%M")

last_date = inspections_date
if last_date < patients_date:
    last_date = patients_date
last_date_str = last_date.strftime("%Y/%m/%d %H:%M")

# data.json 雛形
data = {
    # 検査実施数
    "inspections": {
        "date": inspections_date_str,
        "data": inspections
    },
    "inspections_summary": {
        "date": inspections_date_str,
        "data": inspections_summary_data,
        "labels": inspections_summary_labels
    },
    # 感染者数
    "patients": {
        "date": patients_date_str,
        "data": patients
    },
    "patients_summary": {
        "date": patients_date_str,
        "data": patients_summary_data,
        "labels": patients_summary_labels
    },
    "lastUpdate": last_date_str
}

print(json.dumps(data))
