from helpers import get_top_areas

import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scrappers import scrape_top_areas

if __name__ == '__main__':
    driver = webdriver.Chrome()

    driver.get("https://www.nawy.com/")

    top_area = get_top_areas(driver)

    scrape_top_areas(driver, top_area)

