#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import argparse

from utils import *
from utils_industry import *


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
    print(data)
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


def readSubtitles(name):
    print(f'\n\n\n*******************\nRead Subtitles file:{name}\n')
    data = {}
    try:
        with open(name) as file:
            line = file.readline().strip()
            index = 0
            while line:
                # print(f'Line {index}: [{line}]')
                names = line.split(":")
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


def createFilters(
        categories,
        categoryDiscoveryList,
        categoryNameMapper,
        filterElevationAmount,
        filterIcons,
        index,
        industryId,
        scenario,
        seasonal
):
    print(f"\nbuild filters {index} for {industryId}")
    filters = []
    for categoryDisplayName, searchQuery in categories[index].items():
        if searchQuery == '/':
            category_name = categoryDisplayName
            if category_name in categoryNameMapper:
                category_name = categoryNameMapper[category_name]
                print(f'++++++ map {categoryDisplayName} to {category_name}')
            category_id = findCategoryId(category_name, categoryDiscoveryList)
            # print(f"\t{category_name}:{category_id}")
            node = createCategoryFilter(categoryDisplayName, category_id)
            # print(f"\t{node}")
            append2Filter(filters, node)
        else:
            # print(f"\t{categoryDisplayName}:{searchQuery}")
            node = createScenarioFilter(categoryDisplayName, searchQuery, filterElevationAmount)
            # print(f"\t{node}")
            append2Filter(filters, node)
    new_line = True
    for season in seasonal:
        node = createSeasonalFilter(season, filterElevationAmount, filterIcons, new_line)
        # print(f"\t{node}")
        new_line = False
        append2Filter(filters, node)
    for key, value in scenario[index].items():
        node = createScenarioFilter(key, value, filterElevationAmount)
        # print(f"\t{node}")
        append2Filter(filters, node)
    # print(f'{filters}')
    print(*filters, sep='\n')
    return filters


def buildIndustriesWithFilters(
        industries,
        categoryDiscoveryList,
        categoryNameMapper,
        industryIds,
        categories,
        seasonal,
        scenario,
        filterElevationAmount,
        filterIcons,
        subtitles
):
    print(f'\n\n\n*******************\nbuild industries with filters file\n')
    # print(f"build {industryIds}")
    total_industries = len(industryIds)
    # print(f"total_industries: {total_industries}")
    industry_list = industries['industries']
    for index in range(total_industries):
        industry_id = industryIds[index]
        filters = createFilters(
            categories,
            categoryDiscoveryList,
            categoryNameMapper,
            filterElevationAmount,
            filterIcons,
            index,
            industry_id,
            scenario,
            seasonal)
        industry = industry_list[findIndustryIndex(industry_id, industry_list)]
        if industry_id in subtitles:
            industry['subtitle'] = subtitles[industry_id]
        industry['filters'] = filters
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
parser.add_argument('--subtitles', '-st', help='subtitles file 属性，非必要参数', required=False)
parser.add_argument('--out', '-o', help='output json file 属性，非必要参数', required=False)
args = parser.parse_args()

if __name__ == '__main__':
    try:
        specialPath = "improvement/"

        baseFilesPath = f"files/"
        baseFilesSpecialPath = f"files/{specialPath}"
        industries = args.industries or f"{baseFilesSpecialPath}industries.json"
        industryIds = args.industryIds or f"{baseFilesSpecialPath}industry_ids.txt"
        categoryDiscoveryList = args.categoryDiscoveryList or f"{baseFilesPath}categoryDiscoveryList.json"
        subtitles = args.subtitles or f"{baseFilesSpecialPath}subtitles.properties"

        filtersPath = "filters/"
        filtersSpecialPath = f"filters/{specialPath}"
        category = args.category or f"{filtersSpecialPath}categories"
        scenario = args.scenario or f"{filtersSpecialPath}scenario_keywords"
        categoryNameMapper = args.categoryNameMapper or f"{filtersPath}category_name_mapper.txt"
        seasonal = args.seasonal or f"{filtersPath}seasonal_keywords"
        filterElevationAmount = args.filterElevationAmount or f"{filtersPath}filter_elevation_amount"
        filterIcons = args.filterIcons or f"{filtersPath}filter_icons"

        industriesAfter = args.out or f"./out/industries_{getCurrentTimestamp()}.json"

        print(f"""
        categoryDiscoveryList file: {categoryDiscoveryList}
        industries file: {industries}
        industryIds file: {industryIds}
        category name mapper file: {categoryNameMapper}
        category file: {category}
        seasonal file: {seasonal}
        scenario file: {scenario}
        filter elevation amount file: {filterElevationAmount}
        subtitles file: {subtitles}
        industriesAfter file: {industriesAfter}
        """)

        categoryDiscoveryList = readJson(categoryDiscoveryList)
        industries = readJson(industries)
        industryIds = readIndustryIds(industryIds)
        subtitles = readSubtitles(subtitles)

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
            filterIcons,
            subtitles
        )
        saveIndustries(industries, industriesAfter)
    except Exception as e:
        print(e)
