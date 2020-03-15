import os
import datetime


def debug(name, msg):
    if os.environ.get('IS_DEBUG', False):
        print('[DEBUG {} {}] {}'.format(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"), name, msg))


def warning(name, msg):
    print('[WARNING {} {}] {}'.format(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"), name, msg))
