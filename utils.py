import os
import datetime


def debug(name, msg):
    if os.environ.get('IS_DEBUG', False):
        print('[{} {}] {}'.format(datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"), name, msg))