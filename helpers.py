import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_top_areas(driver):
    try:
        # select all areas
        top_areas = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "area-dev-card"))
        )
        area_links = [area.get_attribute("href") for area in top_areas]

    except Exception as e:
        print("Area Not Found due to exception:", e)

    return area_links


def get_area_compounds(driver, area):
    driver.get(area)
    compounds_link = []
    prev_page_url = None

    while True:
        # Explicit wait for the next page button
        curr_page_compounds = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-cy="card-link"]')))

        page_compound_links = [curr_page_compound_links.get_attribute("href") for curr_page_compound_links in
                               curr_page_compounds]
        compounds_link.extend(page_compound_links)

        try:
            element = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".next-arrow.pagination-list"))
            )
            element.click()

            # Wait for the current page's compounds_link to load

            curr_page_url = driver.current_url
            if curr_page_url == prev_page_url:
                break
            prev_page_url = curr_page_url
        except:
            break

    # Print the final count of compounds_link
    print("Total compounds_link:", len(compounds_link))
    return compounds_link
    # scrape_compounds(compounds_link)