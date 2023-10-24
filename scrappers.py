import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import get_area_compounds, get_types_of_properties, get_compound_properties


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


