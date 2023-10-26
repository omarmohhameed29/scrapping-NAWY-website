import time

from helpers import get_area_compounds, get_types_of_properties, get_compound_properties, get_properties_data


def scrape_top_areas(driver, top_areas):
    for area in top_areas:
        area_compounds = get_area_compounds(driver, area)
        scrape_area_compounds(driver, area_compounds)


def scrape_area_compounds(driver, area_compounds):
    for compound in area_compounds:
        scrape_compound_properties(driver, compound)


def scrape_compound_properties(driver, compound):
    driver.get(compound)

    # select all types of properties
    types_of_properties = get_types_of_properties(driver)

    # Iterate through property types and click on them
    for i in range(len(types_of_properties)):
        get_compound_properties(compound, types_of_properties, driver)


def scrape_current_page(driver):
    get_properties_data(driver)

    # minute sleep to avoid session blocking
    time.sleep(60)
