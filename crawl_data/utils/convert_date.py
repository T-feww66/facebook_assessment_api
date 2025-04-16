from datetime import datetime, timedelta
import re
import calendar

from datetime import datetime, timedelta
import re
import calendar

def convert_time_label_to_date(label, date_now):
    now = datetime.strptime(date_now, "%d/%m/%Y")
    label = label.lower().strip()

    number_search = re.search(r"\d+", label)
    number = int(number_search.group()) if number_search else 1

    if "hôm qua" in label:
        return (now - timedelta(days=1)).strftime("%d/%m/%Y")
    elif "hôm kia" in label:
        return (now - timedelta(days=2)).strftime("%d/%m/%Y")
    elif "ngày" in label:
        return (now - timedelta(days=number)).strftime("%d/%m/%Y")
    elif "tuần" in label:
        return (now - timedelta(weeks=number)).strftime("%d/%m/%Y")
    elif "tháng" in label:
        new_month = now.month - number
        new_year = now.year
        while new_month <= 0:
            new_month += 12
            new_year -= 1
        last_day = calendar.monthrange(new_year, new_month)[1]
        day = min(now.day, last_day)
        return datetime(new_year, new_month, day).strftime("%d/%m/%Y")
    elif "năm" in label:
        try:
            return now.replace(year=now.year - number).strftime("%d/%m/%Y")
        except ValueError:
            return now.replace(year=now.year - number, day=28).strftime("%d/%m/%Y")
    elif "giờ" in label or "phút" in label or "vừa xong" in label:
        return now.strftime("%d/%m/%Y")
    else:
        return now.strftime("%d/%m/%Y")