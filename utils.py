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


def readSimpleLineFile(name):
    data = []
    try:
        with open(name) as file:
            line = file.readline().strip()
            index = 0
            while line:
                # print(f'Line {index}: [{line}]')
                data.append(line)
                index += 1
                line = file.readline().strip()
    except Exception as e:
        print(e)
        raise
    finally:
        file.close()
    print(*data, sep='\n')
    return data


def readPropertiesFile(name):
    separator = ":"
    data = {}
    try:
        with open(name) as file:
            line = file.readline().strip()
            index = 0
            while line:
                # print(f'Line {index}: [{line}]')
                names = line.split(separator, 1)
                data[names[0]] = names[1]
                index += 1
                line = file.readline().strip()
    except Exception as e:
        print(e)
        raise
    finally:
        file.close()
    print(data)
    return data


def readComplexFile(name):
    data = []
    try:
        with open(name) as file:
            line = file.readline().strip()
            index = 0
            while line:
                # print(f'Line {index}: [{line}]')
                names = line.split("\t")
                item = transform2Map(names)
                data.append(item)
                index += 1
                line = file.readline().strip()
    except Exception as e:
        print(e)
        raise
    finally:
        file.close()
    print(*data, sep='\n')
    return data
