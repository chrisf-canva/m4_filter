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


def readFilterDefault(name):
    print(f'\n\n\n*******************\nRead filter default file:{name}\n')
    return readPropertiesFileAsArray(name)


def createFilters(industry_id, index_of_industry, categories, scenario, seasonal, category_discovery_list,
                  category_name_mapper, filter_elevation_amount, filter_icons, filterDefault):
    print(f"\nbuild filters {index_of_industry} for {industry_id}")
    filters = []
    for display_name, search_query in filterDefault[index_of_industry].items():
        node = createDefaultFilter(display_name, search_query)
        # print(f"\t{node}")
        appendToDict(filters, node)
    for category_display_name, search_query in categories[index_of_industry].items():
        node = createCategoryNode(category_discovery_list, category_display_name, category_name_mapper, industry_id,
                                  search_query)
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
        node = createCategoryNode(category_discovery_list, category_display_name, category_name_mapper, industry_id,
                                  search_query)
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
        carousel_category_all,
        filterDefault
):
    print(f'\n\n\n*******************\nbuild industries with filters file\n')
    # print(f"build {industryIds}")
    total_industries = len(industryIds)
    # print(f"total_industries: {total_industries}")
    industry_list = industries['industries']
    for index in range(total_industries):
        industry_id = industryIds[index]
        filters = createFilters(industry_id, index, categories, scenario, seasonal, categoryDiscoveryList,
                                categoryNameMapper, filterElevationAmount, filterIcons, filterDefault)
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
parser.add_argument('--industries', '-in', help='industry json file 属性，非必要参数', required=False)
parser.add_argument('--industryIds', '-inid', help='industry ID file 属性，非必要参数', required=False)
parser.add_argument('--categoryDiscoveryList', '-cdf', help='category discovery jons file 属性，非必要参数', required=False)
parser.add_argument('--categoryNameMapper', '-cn', help='category name mapper file 属性，非必要参数', required=False)
parser.add_argument('--category', '-cf', help='category filter file 属性，非必要参数', required=False)
parser.add_argument('--seasonal', '-ss', help='seasonal filter file 属性，非必要参数', required=False)
parser.add_argument('--scenario', '-sf', help='scenario filter file 属性，非必要参数', required=False)
parser.add_argument('--filterElevationAmount', '-fea', help='filter elevation amount file 属性，非必要参数', required=False)
parser.add_argument('--filterIcons', '-fi', help='filter icons file 属性，非必要参数', required=False)
parser.add_argument('--filter_default', '-fd', help='filter default file 属性，非必要参数', required=False)
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
        industryIds = args.industryIds or f"{baseFilesSpecialPath}industry_ids"
        subtitles = args.subtitles or f"{baseFilesSpecialPath}subtitles.properties"
        categoryDiscoveryList = args.categoryDiscoveryList or f"{baseFilesPath}categoryDiscoveryList.json"

        filtersPath = "filters/"
        filtersSpecialPath = f"filters/{specialPath}"
        filterDefault = args.filter_default or f"{filtersSpecialPath}filter_default.properties"
        category = args.category or f"{filtersSpecialPath}categories"
        seasonal = args.seasonal or f"{filtersPath}seasonal_keywords"
        scenario = args.scenario or f"{filtersSpecialPath}scenario_keywords"
        categoryNameMapper = args.categoryNameMapper or f"{filtersPath}category_name_mapper.properties"
        filterElevationAmount = args.filterElevationAmount or f"{filtersPath}filter_elevation_amount"
        filterIcons = args.filterIcons or f"{filtersPath}filter_icons.properties"

        carouselsPath = "carousel/"
        carousel_categories = args.carousel_category or f"{carouselsPath}categories"
        carousel_category_all = args.carousel_category_all or f"{carouselsPath}category_for_all.properties"

        industries_out = args.out or f"./out/industries_{getCurrentTimestamp()}.json"

        print(f"""
        industries file: {industries}
        industryIds file: {industryIds}
        subtitles file: {subtitles}
        categoryDiscoveryList file: {categoryDiscoveryList}
     
        filter default file: {filterDefault}
        category file: {category}
        seasonal file: {seasonal}
        scenario file: {scenario}
        category name mapper file: {categoryNameMapper}
        filter elevation amount file: {filterElevationAmount}
        filter icon file: {filterIcons}
     
        carousel category file: {carousel_categories}
        carousel category for all file: {carousel_category_all}
     
        industries output file: {industries_out}
        """)

        industries = readJson(industries)
        industryIds = readIndustryIds(industryIds)
        subtitles = readSubtitles(subtitles)
        categoryDiscoveryList = readJson(categoryDiscoveryList)

        filterDefault = readFilterDefault(filterDefault)
        category = readCategoryPills(category)
        seasonal = readSeasonal(seasonal)
        scenario = readScenario(scenario)
        categoryNameMapper = readCategoryNameMapper(categoryNameMapper)
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
            carousel_category_all,
            filterDefault
        )
        saveIndustries(industries, industries_out)
    except Exception as e:
        print(e)
