import time
import re
import pandas as pd
from selenium.webdriver.common.by import By


data = pd.DataFrame(columns=['Bedrooms', 'Bathrooms', 'Area', 'Price', 'Location', 'Property Type', 'Compound'])


def Extract(property_cards):
    # todo extract area, compound name
    for property_card in property_cards:

        num_bedrooms, num_bathrooms = extract_rooms_details(property_card)

        area = extract_area(property_card)

        price = extract_price(property_card)

        location = extract_location(property_card)

        property_type, compound = extract_property_type_and_compound_name(property_card)

        extracted_data = [num_bedrooms, num_bathrooms, area, price, location, property_type, compound]

        Load(extracted_data)


def Transform(extracted_data):
    pass


def Load(extracted_data):
    print('Loading')
    num_bedrooms = extracted_data[0]
    num_bathrooms = extracted_data[1]
    area = extracted_data[2]
    price = extracted_data[3]
    location = extracted_data[4]
    property = extracted_data[5]
    compound = extracted_data[6]
    print('Storing')
    new_record = {'Bedrooms': num_bedrooms,
                  'Bathrooms': num_bathrooms,
                  'Area': area,
                  'Price': price,
                  'Location': location,
                  'Property Type': property,
                  'Compound': compound}
    print("new_record:", new_record)

    # append new record to data DF
    global data
    data = pd.concat([data, pd.DataFrame([new_record])], ignore_index=True)
    print(data)



def extract_rooms_details(property_card):
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

    return num_bedrooms, num_bathrooms


def extract_area(property_card):
    # get area in sq_meters
    area_details = property_card.find_element(By.CLASS_NAME, "type_area")
    span_area = area_details.find_element(By.TAG_NAME, "span")
    area = re.findall(r'\d+', span_area.get_attribute("innerHTML"))[0]
    print("area:", area)
    return area



def extract_price(property_card):
    price_details = property_card.find_element(By.CLASS_NAME, "price")
    div_price = price_details.find_element(By.TAG_NAME, "div")
    price = div_price.get_attribute("innerHTML")
    print("price:", price)
    return price


def extract_location(property_card):
    location_details = property_card.find_element(By.CLASS_NAME, "location")
    location = location_details.get_attribute("innerHTML")
    print("location:", location)
    return location


def extract_property_type_and_compound_name(property_card):
    property_element = property_card.find_element(By.CSS_SELECTOR, '[data-cy="card-title"]')
    property_inner_text = property_element.get_attribute('innerHTML')
    text = property_inner_text.split(' - ')
    property_type = text[0]
    print('Property Type:', property_type)
    compound = text[1]
    return property_type, compound


