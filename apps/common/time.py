# -*- coding: utf-8 -*-
from datetime import datetime
from pytz import timezone, utc

KST = timezone('Asia/Seoul')


def utc_to_local(t):
    if type(t) == 'str':
        t = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
    return utc.localize(t).astimezone(KST)
