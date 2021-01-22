#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from utils import filterNone


def appendToDict(filters, node):
    filters.append(node)


def create_category_for_carousel(displayName, categoryId, searchQuery):
    type = "scenario" if categoryId is None else "category"
    node = {
        'title': displayName,
        "type": type,
        "categoryId": categoryId,
        "searchQuery": searchQuery
    }
    return filterNone(node)


def createCategoryFilter(displayName, categoryId):
    return {
        'title': displayName,
        "type": "category",
        "categoryId": categoryId
    }


def createScenarioFilter(displayName, searchQuery, filterElevationAmount):
    node = {
        'title': displayName,
        "type": "scenario",
        "searchQuery": searchQuery
    }
    if (searchQuery in filterElevationAmount):
        node["elevationAmount"] = int(filterElevationAmount[searchQuery])
    return node


def createSeasonalFilter(displayName, filterElevationAmount, filterIcons, newLine=False):
    node = {
        'title': displayName,
        "type": "seasonal",
        "searchQuery": displayName
    }
    if (displayName in filterElevationAmount):
        node["elevationAmount"] = int(filterElevationAmount[displayName])
    if (displayName in filterIcons):
        node["iconUrl"] = filterIcons[displayName]
    if (newLine):
        node['newLine'] = newLine
    return node


def findIndustryIndex(industryId, industryList):
    num = len(industryList)
    index = next(index for index in range(num) if industryList[index]['key'].lower() == industryId.lower())
    # print(f"found {industryId}'s index: {index}")
    return index


def findCategoryId(name, dict):
    category = None
    try:
        results = dict['results']
        # print(f"looking for name :[{name}]")
        node = list(filter(lambda x: x['categoryDisplayName'].lower() == name.lower(), results))[0]
        category = node['category']
        # print(f"category: {category}")
    except Exception as e:
        print(f"""

\t***********************************
\tfailed to find category id for {name}: {e}
\t***********************************

""")
    return category
