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


def createDefaultFilter(displayName, searchQuery):
    return {
        'title': displayName,
        "type": "default",
        "searchQuery": searchQuery
    }


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


def find_category_name(category_display_name, category_name_mapper, industry_id):
    category_name = category_display_name
    if category_name in category_name_mapper:
        name = category_name_mapper[category_name]
        names = name.split("/", 1)
        if len(names) == 2:
            if names[0] == industry_id:
                category_name = names[1]
                print(f"""
++++++ find category name: {category_name} by {name} of {industry_id}
                """)
        else:
            category_name = name
            print(f"""
++++++ find category name: {category_name} by display name {category_display_name}
            """)
    return category_name


def createCategoryNode(category_discovery_list, category_display_name, category_name_mapper, industry_id, search_query):
    # print(f"\t{category_display_name}:{search_query}")
    if search_query.startswith('/') and len(search_query) > 1:
        category_id = None
        search_query = search_query[1:]
        print(f"""
++++++ find search query: {search_query} started with /
        """)
        # print(f"\t{category_id}:{search_query}")
    else:
        category_name = find_category_name(category_display_name, category_name_mapper, industry_id)
        # find category id
        category_id = findCategoryId(category_name, category_discovery_list)
        # print(f"\t{category_name}:{category_id}")
        if search_query == '/':
            search_query = None
    # print(f"\t{category_id}:{category_display_name}:{search_query}")
    node = create_category_for_carousel(category_display_name, category_id, search_query)
    # print(f"\t\t{node}")
    return node
