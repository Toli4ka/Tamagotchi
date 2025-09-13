try:
    import utime as time
except ImportError:
    import datetime
    time = None

def _now_yymmdd():
    if time:
        y, m, d, hh, mm, ss, wd, yd = time.localtime()
        return "{:02d}{:02d}{:02d}".format(y % 100, m, d)
    return datetime.datetime.now().strftime("%y%m%d")

def _now_hour():
    if time:
        return "{:02d}".format(time.localtime()[3])
    return datetime.datetime.now().strftime("%H")

def _now_yymmddhhmm():
    if time:
        y, m, d, hh, mm, ss, wd, yd = time.localtime()
        return "{:02d}{:02d}{:02d}{:02d}{:02d}".format(y % 100, m, d, hh, mm)
    return datetime.datetime.now().strftime("%y%m%d%H%M")
