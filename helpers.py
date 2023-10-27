import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ELT import Extract, save_data_in_csv_file


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


def scrape_properties(driver):
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
    Extract(property_cards)


def no_next_properties_page(driver):
    # check for next page

    # handle case when there is no disabled buttons yet in the screen
    try:
        disabled_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".next-arrow.pagination-list.disabled"))
        )
    except Exception as e:
        disabled_buttons = [0]

    enabled_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".next-arrow.pagination-list"))
    )
    print('len of enabled buttons:',len(enabled_buttons))
    print('len of disabled buttons:',len(disabled_buttons))
    if len(disabled_buttons) == len(enabled_buttons):
        return True

    for enabled_button in enabled_buttons:
        if enabled_button not in disabled_buttons:
            print('clicked on next button')
            enabled_button.click()
            return False
    # except Exception as e:
    #     # todo fix error in sarai madinet nasr
    #     print("couldn't load next page:", e)
    #     save_data_in_csv_file()
    #     quit()

