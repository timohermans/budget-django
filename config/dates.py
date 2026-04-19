import calendar


def subtract_one_month(d):
    month = d.month - 1 or 12
    year = d.year - (1 if d.month == 1 else 0)
    day = min(d.day, calendar.monthrange(year, month)[1])
    return d.replace(year=year, month=month, day=day)