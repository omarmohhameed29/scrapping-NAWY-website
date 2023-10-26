import time
import re
import pandas as pd
from selenium.webdriver.common.by import By


data = pd.DataFrame(columns=['Bedrooms', 'Bathrooms', 'Area', 'Price', 'Location'])


def Extract(property_cards):
    # todo extract area, compound name
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


        location_details = property_card.find_element(By.CLASS_NAME, "location")
        location = location_details.get_attribute("innerHTML")
        extracted_data = [num_bedrooms, num_bathrooms, area, price, location]
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
    print('Storing')
    new_record = {'Bedrooms': num_bedrooms, 'Bathrooms': num_bathrooms, 'Area': area, 'Price': price, 'Location': location}
    print("new_record:", new_record)

    # append new record to data DF
    global data
    data = pd.concat([data, pd.DataFrame([new_record])], ignore_index=True)
    print(data)
