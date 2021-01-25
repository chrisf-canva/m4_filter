#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import argparse

from utils import *
from utils_industry import *


def readIndustryIds(name):
    print(f'\n\n\n*******************\nRead Industry Id file:{name}\n')
    return readSimpleLineFile(name)


def readCategoryNameMapper(name):
    print(f'\n\n\n*******************\nRead Category name mapper file:{name}\n')
    return readPropertiesFile(name)


def readCategoryPills(name):
    print(f'\n\n\n*******************\nRead Category pills file:{name}\n')
    return readComplexFile(name)


def readSeasonal(name):
    print(f'\n\n\n*******************\nRead Seasonal file:{name}\n')
    return readSimpleLineFile(name)


def readScenario(name):
    print(f'\n\n\n*******************\nRead Scenario file:{name}\n')
    return readComplexFile(name)


def readFilterElevationAmount(name):
    print(f'\n\n\n*******************\nRead Filter Elevation Amount file:{name}\n')
    return readComplexFile(name)[0]


def readFilterIcons(name):
    print(f'\n\n\n*******************\nRead Filter Icons file:{name}\n')
    return readPropertiesFile(name)


def readSubtitles(name):
    print(f'\n\n\n*******************\nRead Subtitles file:{name}\n')
    return readPropertiesFile(name)


def readCarouselForAll(name):
    print(f'\n\n\n*******************\nRead carousel category for all file:{name}\n')
    return readPropertiesFile(name)


def createFilters(industry_id, index_of_industry, categories, scenario, seasonal, category_discovery_list,
                  category_name_mapper, filter_elevation_amount, filter_icons):
    print(f"\nbuild filters {index_of_industry} for {industry_id}")
    filters = []
    for categoryDisplayName, searchQuery in categories[index_of_industry].items():
        if searchQuery == '/':
            category_name = categoryDisplayName
            if category_name in category_name_mapper:
                category_name = category_name_mapper[category_name]
                print(f'++++++ map {categoryDisplayName} to {category_name}')
            category_id = findCategoryId(category_name, category_discovery_list)
            # print(f"\t{category_name}:{category_id}")
            node = createCategoryFilter(categoryDisplayName, category_id)
            # print(f"\t{node}")
            appendToDict(filters, node)
        else:
            # print(f"\t{categoryDisplayName}:{searchQuery}")
            node = createScenarioFilter(categoryDisplayName, searchQuery, filter_elevation_amount)
            # print(f"\t{node}")
            appendToDict(filters, node)
    new_line = True
    for season in seasonal:
        node = createSeasonalFilter(season, filter_elevation_amount, filter_icons, new_line)
        # print(f"\t{node}")
        new_line = False
        appendToDict(filters, node)
    for key, value in scenario[index_of_industry].items():
        node = createScenarioFilter(key, value, filter_elevation_amount)
        # print(f"\t{node}")
        appendToDict(filters, node)
    # print(f'{filters}')
    print(*filters, sep='\n')
    return filters


def createCarousels(categories, carousel_category_all, industry_id, index_of_industry, category_discovery_list,
                    category_name_mapper):
    print(f"\nbuild carousels {index_of_industry} for {industry_id}")
    carousels = []
    for category_display_name, search_query in categories[index_of_industry].items():
        # print(f"\t{category_display_name}:{search_query}")
        # find category id
        category_name = category_display_name
        if category_name in category_name_mapper:
            category_name = category_name_mapper[category_name]
            print(f'++++++ find category name: {category_name} by display name {category_display_name}')
        category_id = findCategoryId(category_name, category_discovery_list)
        # print(f"\t{category_name}:{category_id}")
        if search_query == '/':
            search_query = None
        node = create_category_for_carousel(category_display_name, category_id, search_query)
        # print(f"\t\t{node}")
        appendToDict(carousels, node)
    for category_name, category_id in carousel_category_all.items():
        node = create_category_for_carousel(category_name, category_id, None)
        appendToDict(carousels, node)
    print(*carousels, sep='\n')
    return carousels


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
        subtitles,
        carousel_categories,
        carousel_category_all
):
    print(f'\n\n\n*******************\nbuild industries with filters file\n')
    # print(f"build {industryIds}")
    total_industries = len(industryIds)
    # print(f"total_industries: {total_industries}")
    industry_list = industries['industries']
    for index in range(total_industries):
        industry_id = industryIds[index]
        filters = createFilters(industry_id, index, categories, scenario, seasonal, categoryDiscoveryList,
                                categoryNameMapper, filterElevationAmount, filterIcons)
        carousels = createCarousels(carousel_categories, carousel_category_all, industry_id, index,
                                    categoryDiscoveryList, categoryNameMapper)
        industry = industry_list[findIndustryIndex(industry_id, industry_list)]
        if industry_id in subtitles:
            industry['subtitle'] = subtitles[industry_id]
        industry['filters'] = filters
        industry['carousels'] = carousels
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
parser.add_argument('--carousel_category', '-cc', help='carousel category file 属性，非必要参数', required=False)
parser.add_argument('--carousel_category_all', '-cca', help='carousel category for all file 属性，非必要参数', required=False)
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
        categoryNameMapper = args.categoryNameMapper or f"{filtersPath}category_name_mapper.properties"
        seasonal = args.seasonal or f"{filtersPath}seasonal_keywords"
        filterElevationAmount = args.filterElevationAmount or f"{filtersPath}filter_elevation_amount"
        filterIcons = args.filterIcons or f"{filtersPath}filter_icons.properties"

        carouselsPath = "carousel/"
        carousel_categories = args.carousel_category or f"{carouselsPath}categories"
        carousel_category_all = args.carousel_category_all or f"{carouselsPath}category_for_all.properties"

        industries_out = args.out or f"./out/industries_{getCurrentTimestamp()}.json"

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
        carousel category file: {carousel_categories}
        carousel category for all file: {carousel_category_all}
        industries output file: {industries_out}
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

        carousel_categories = readCategoryPills(carousel_categories)
        carousel_category_all = readCarouselForAll(carousel_category_all)

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
            subtitles,
            carousel_categories,
            carousel_category_all
        )
        saveIndustries(industries, industries_out)
    except Exception as e:
        print(e)
