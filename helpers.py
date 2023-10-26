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

    while True:
        # Explicit wait for the next page button
        curr_page_compounds = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-cy="card-link"]')))

        page_compound_links = [curr_page_compound_links.get_attribute("href") for curr_page_compound_links in
                               curr_page_compounds]
        compounds_link.extend(page_compound_links)

        curr_page_url = driver.current_url
        if no_next_page(driver, curr_page_url):
            break

    print("Total compounds_link:", len(compounds_link))
    return compounds_link


def no_next_page(driver, curr_page_url):
    try:
        element = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".next-arrow.pagination-list"))
        )
        element.click()

        # Wait for the current page's compounds_link to load

        return curr_page_url == driver.current_url
    except Exception as e:
        print("Couldn't check next page,", e)


def get_types_of_properties(driver):
    types_of_properties = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-58c97ab0-0"))
    )
    return types_of_properties


def get_compound_properties(compound, types_of_properties, driver):
    # Re-fetch the elements on each iteration to avoid StaleElementReferenceException
    for i in range(len(types_of_properties)):
        types_of_properties = get_types_of_properties(driver)
        types_of_properties[i].click()
        print("Clicked on property type:", i)

        scrape_properties(driver)
        print("current page scraped successfully")
        # Wait for the page to load new data (you may need to adjust this)
        time.sleep(2)

        driver.get(compound)
        print("get back to compound initial page at index:", i)

        # Wait for the page to load (again, adjust timing if needed)
        time.sleep(2)

    print("number of properties:", len(types_of_properties))


# todo refactor scrape_current_page
def scrape_properties(driver):
    # todo scrape the content of each store them in pandas DataFrame to be extracted as CSV file later for analysis
    # todo get the city, region(compound) of each property
    while True:
        try:
            property_cards = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-cy="property-grid-card"]'))
            )
            print("number of properties:", len(property_cards))

            get_properties_data(property_cards)

        except Exception as e:
            print("Property Not Found*", e)

        # check for next page
        if no_next_properties_page(driver):
            break


def get_properties_data(property_cards):
    for property_card in property_cards:
        # check living-apartment vs office
        try:
            bed_room_details = property_card.find_element(By.CLASS_NAME, "bedroominnerdetails")
            num_bedrooms = bed_room_details.find_element(By.TAG_NAME, "p").get_attribute("innerHTML")
            print("num_bedrooms:", num_bedrooms)

            # get number of bathrooms
            bath_room_details = property_card.find_element(By.CLASS_NAME, "bathroominnerdetails")
            num_bathrooms = bath_room_details.find_element(By.TAG_NAME, "p").get_attribute("innerHTML")
            print("num_bathrooms:", num_bathrooms)

        except:
            print("not living apartment")
            num_bedrooms = 0
            num_bathrooms = 0
        # get area in sq_meters
        area_details = property_card.find_element(By.CLASS_NAME, "type_area")
        span_area = area_details.find_element(By.TAG_NAME, "span")
        area = re.findall(r'\d+', span_area.get_attribute("innerHTML"))[0]
        print("area:", area)

        # get price
        price_details = property_card.find_element(By.CLASS_NAME, "price")
        div_price = price_details.find_element(By.TAG_NAME, "div")
        price = div_price.get_attribute("innerHTML")
        print("price:", price)


def no_next_properties_page(driver):
    # check for next page
    try:
        next_page = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".next-arrow.pagination-list.disabled"))
        )
        if len(next_page) == 2:
            print("Last Page")
            return True
    except Exception as e:
        print("couldn't load next page:", e)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".next-arrow.pagination-list"))
        )
        # element = element[-1]
        if len(element) == 2:
            try:
                element[-1].click()
            except:
                element[0].click()
        else:
            return True
    except Exception as e:
        print("error:", e)
