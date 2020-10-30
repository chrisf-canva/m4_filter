#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import argparse
import re
import json

def readIndustryIds(name):
    print(f'\n\n\n*******************\nRead Industry Id file:{name}\n')
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

def readCategoryNameMapper(name):
    print(f'\n\n\n*******************\nRead Category name mapper file:{name}\n')
    data = {}
    try:
        with open(name) as file:
                line = file.readline().strip()
                index = 0
                while line:
                    # print(f'Line {index}: [{line}]')
                    names = line.split("\t")
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

def readCategoryPills(name):
    print(f'\n\n\n*******************\nRead Category pills file:{name}\n')
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

def readSeasonal(name):
    print(f'\n\n\n*******************\nRead Seasonal file:{name}\n')
    data = []
    try:
        with open(name) as file:
                line = file.readline().strip()
                index = 0
                while line:
                    # print(f'Line {index}: [{line}]')
                    names = line.split("\t")
                    for name in names:
                        data.append(name)
                    index += 1
                    line = file.readline().strip()
    except Exception as e:
        print(e)
        raise
    finally:
        file.close()
    print(*data, sep='\n')
    return data

def readScenario(name):
    print(f'\n\n\n*******************\nRead Scenario file:{name}\n')
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

def readFilterElevationAmount(name):
    print(f'\n\n\n*******************\nRead Filter Elevation Amount file:{name}\n')
    data = {}
    try:
        with open(name) as file:
                line = file.readline().strip()
                index = 0
                while line:
                    # print(f'Line {index}: [{line}]')
                    names = line.split("\t")
                    item = transform2Map(names)
                    data.update(item)
                    index += 1
                    line = file.readline().strip()
    except Exception as e:
        print(e)
        raise
    finally:
        file.close()
    print(*data, sep='\n')
    return data

def readFilterIcons(name):
    print(f'\n\n\n*******************\nRead Filter Icons file:{name}\n')
    data = {}
    try:
        with open(name) as file:
                line = file.readline().strip()
                index = 0
                while line:
                    # print(f'Line {index}: [{line}]')
                    names = line.split("\t")
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

def buildIndustriesWithFilters(
            industries,
            categoryDiscoveryList,
            categoryNameMapper,
            industryIds,
            categories,
            seasonal,
            scenario,
            filterElevationAmount,
            filterIcons
        ):
    print(f'\n\n\n*******************\nbuild industries with filters file\n')
    # print(f"build {industryIds}")
    totalIndustries = len(industryIds)
    # print(f"totalIndustries: {totalIndustries}")
    industryList = industries['industries']
    for index in range(totalIndustries):
        industryId = industryIds[index]
        print(f"\nbuild {index}: {industryId}")
        filters = []
        for categoryDisplayName, searchQuery in categories[index].items():
            if (searchQuery == '/'):
                categoryName = categoryDisplayName
                if categoryName in categoryNameMapper:
                    categoryName = categoryNameMapper[categoryName]
                    print(f'++++++ map {categoryDisplayName} to {categoryName}')
                categoryId = findCategoryId(categoryName, categoryDiscoveryList)
                # print(f"\t{categoryName}:{categoryId}")
                node = createCategoryFilter(categoryDisplayName, categoryId)
                print(f"\t{node}")
                append2Filter(filters, node)
            else:
                # print(f"\t{categoryDisplayName}:{searchQuery}")
                node = createScenarioFilter(categoryDisplayName, searchQuery, filterElevationAmount)
                print(f"\t{node}")
                append2Filter(filters, node)
        newLine = True
        for season in seasonal:
            node = createSeasonalFilter(season, filterElevationAmount, filterIcons, newLine)
            print(f"\t{node}")
            newLine = False
            append2Filter(filters, node)
        for key, value in scenario[index].items():
            node = createScenarioFilter(key, value, filterElevationAmount)
            print(f"\t{node}")
            append2Filter(filters, node)
        # print(f'{filters}')
        industryList[findIndustryIndex(industryId, industryList)]['filters'] = filters
    return industries

def saveIndustries(industries, out):
    print(f'\n\n\n*******************\nsave industries to {out}\n')
    # print(f"\nindustries:\n{industries}\n\n\n\n\n\n")
    result = json.dumps(industries, indent=2, sort_keys=False)
    # print(f"\n\nNEW industries:\n{result}")
    try:
        with open(out, "w") as file:
            file.write(result)
    except Exception as e:
        print(e)
        raise
    finally:
        file.close()

def append2Filter(filters, node):
    filters.append(node)

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

def createSeasonalFilter(displayName, filterElevationAmount, filterIcons, newLine = False):
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
    print(f"found {industryId}'s index: {index}")
    return index

def findCategoryId(name, dict):
    results = dict['results']
    # print(f"looking for name :[{name}]")
    node = list(filter(lambda x: x['categoryDisplayName'].lower() == name.lower(), results))[0]
    category = node['category']
    # print(f"category: {category}")
    return category

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

parser = argparse.ArgumentParser(description='Test for argparse')
parser.add_argument('--categoryDiscoveryList', '-cdf', help='category discovery jons file 属性，非必要参数', required=False)
parser.add_argument('--industries', '-in', help='industry json file 属性，非必要参数', required=False)
parser.add_argument('--industryIds', '-inid', help='industry ID file 属性，非必要参数', required=False)
parser.add_argument('--categoryNameMapper', '-cn', help='category name mapper file 属性，非必要参数', required=False)
parser.add_argument('--category', '-cf', help='category filter file 属性，非必要参数', required=False)
parser.add_argument('--seasonal', '-ss', help='seasonal filter file 属性，非必要参数', required=False)
parser.add_argument('--scenario', '-sf', help='scenario filter file 属性，非必要参数', required=False)
parser.add_argument('--filterElevationAmount', '-fea', help='filter elevation amount file 属性，非必要参数', required=False)
parser.add_argument('--filterIcons', '-fi', help='filter icons file 属性，非必要参数', required=False)
parser.add_argument('--out', '-o', help='output json file 属性，非必要参数', required=False)
args = parser.parse_args()

if __name__ == '__main__':
    try:
        categoryDiscoveryList = args.categoryDiscoveryList or "./categoryDiscoveryList.json"
        industries = args.industries or "./industries.json"
        industryIds = args.industryIds or "./industry_ids.txt"
        categoryNameMapper = args.categoryNameMapper or "./category_name_mapper.txt"
        category = args.category or "./Category_pills.txt"
        seasonal = args.seasonal or "./Seasonal_keywords.txt"
        scenario = args.scenario or "./Scenario_keywords.txt"
        filterElevationAmount = args.filterElevationAmount or "./filter_elevation_amount.txt"
        filterIcons = args.filterIcons or "./filter_icons"
        industriesAfter = args.out or "./industries_after.json"
        print(f"""
        categoryDiscoveryList file: {categoryDiscoveryList}
        industries file: {industries}
        industryIds file: {industryIds}
        category name mapper file: {categoryNameMapper}
        category file: {category}
        seasonal file: {seasonal}
        scenario file: {scenario}
        filter elevation amount file: {filterElevationAmount}
        industriesAfter file: {industriesAfter}
        """)
        categoryDiscoveryList = readJson(categoryDiscoveryList)
        industries = readJson(industries)
        industryIds = readIndustryIds(industryIds)
        categoryNameMapper = readCategoryNameMapper(categoryNameMapper)
        category = readCategoryPills(category)
        seasonal = readSeasonal(seasonal)
        scenario = readScenario(scenario)
        filterElevationAmount = readFilterElevationAmount(filterElevationAmount)
        filterIcons = readFilterIcons(filterIcons)

        industries = buildIndustriesWithFilters(
            industries,
            categoryDiscoveryList,
            categoryNameMapper,
            industryIds,
            category,
            seasonal,
            scenario,
            filterElevationAmount,
            filterIcons
        )
        saveIndustries(industries, industriesAfter)
    except Exception as e:
        print(e)