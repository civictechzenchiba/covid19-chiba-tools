from datetime import datetime, timedelta
def excel_date(num):
    return (datetime(1899, 12, 30) + timedelta(days=num))
