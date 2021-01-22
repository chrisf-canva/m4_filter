#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import time


def readJson(file):
    return json.load(open(file))


def transform2Map(names):
    num = len(names)
    item = {}
    for i in range(0, num, 2):
        key = names[i].strip()
        value = names[i + 1].strip()
        item[key] = value
    return item


def getCurrentTimestamp():
    time_now = int(time.time())
    time_local = time.localtime(time_now)
    dt = time.strftime("%Y-%m-%d_%H:%M:%S", time_local)
    return dt


def filterNone(original):
    return {k: v for k, v in original.items() if v is not None}
