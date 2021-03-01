import datetime
from datetime import date


def duration_calc(s_date, e_date):
    s_date = s_date.split("-")
    s_date = s_date[2] + s_date[1] + s_date[0] 
    print(s_date) 
    start = datetime.datetime.strptime(s_date, "%d%m%Y").date()

    e_date = e_date.split("-")
    e_date = e_date[2] + e_date[1] + e_date[0]
    end = datetime.datetime.strptime(e_date, "%d%m%Y").date()

    duration = end - start
    return duration.days



