import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import get_area_compounds


def scrape_top_areas(driver, top_areas):
    for area in top_areas:
        compounds = get_area_compounds(driver, area)
