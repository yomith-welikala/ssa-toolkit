import numpy as np


def calendar_to_jd(year, month, day, hour, minute, second):
    anchor = 2451544.5
    y = year - 2000
    sum_year = (y * 365) + np.floor((y - 1) / 4 + 1)

    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if y % 4 == 0:
        days_in_month[2] = 29

    month_sum = sum(days_in_month[1:month])
    d = day - 1
    days_sum = d + month_sum
    fr = (hour + minute / 60 + second / 3600) / 24
    jd = anchor + sum_year + days_sum

    return (jd, fr)


def tle_epoch_to_jd(epoch):
    yy = int(epoch // 1000)
    dd = epoch % 1000

    year = 1900 + yy if yy >= 57 else 2000 + yy
    y = year - 2000

    whole_day = int(dd)
    fr = dd - whole_day

    anchor = 2451544.5
    sum_year = (y * 365) + ((y - 1) // 4 + 1)
    d = whole_day - 1

    jd = anchor + sum_year + d
    return (float(jd), float(fr))
