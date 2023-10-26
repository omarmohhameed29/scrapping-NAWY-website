from ELT import Transform
from helpers import get_top_areas
from selenium import webdriver


from scrappers import scrape_top_areas

if __name__ == '__main__':
    driver = webdriver.Chrome()

    driver.get("https://www.nawy.com/")

    top_area = get_top_areas(driver)

    scrape_top_areas(driver, top_area)

    Transform()

