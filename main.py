from ELT import Transform, save_data_in_csv_file
from helpers import get_top_areas
from selenium import webdriver


from scrappers import scrape_top_areas

if __name__ == '__main__':
    try:
        driver = webdriver.Chrome()

        driver.get("https://www.nawy.com/")
        driver.set_window_size(800, 600)  # Set the window size to a small dimension

        top_area = get_top_areas(driver)

        scrape_top_areas(driver, top_area)

        Transform()

        save_data_in_csv_file()
    except Exception as e:
        print('Final Exception:', e)
        save_data_in_csv_file()

