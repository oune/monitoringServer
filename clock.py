from time import time, localtime, strftime


def get_w_day():
    return localtime(time()).tm_wday


def get_time():
    return strftime('%H:%M:%S', localtime(time()))


def get_date():
    return strftime('%Y%m%d', localtime(time()))


class Time:
    def __init__(self):
        self.pre = get_w_day()

    def is_day_change(self):
        wday = get_w_day()
        ans = wday != self.pre
        self.pre = wday
        return ans

