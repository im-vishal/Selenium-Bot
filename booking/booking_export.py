'''
This file is going to include method that will parse the
specific data that we need from each one of the deal boxes.
'''
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)

class BookingExport:
    def __init__(self, boxes_section_element:WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(
            By.CSS_SELECTOR, 'div[data-testid="property-card"]')

    def pull_deal_box_attributes(self):
        collection = []
        for deal_box in self.deal_boxes:
            # pulling the hotel names
            hotel_name = deal_box.find_element(By.CSS_SELECTOR,
            'div[data-testid="title"]'
            ).get_attribute('innerHTML').strip()

            # pulling the prices
            hotel_price = deal_box.find_element(
                By.CSS_SELECTOR, 'span[class="fcab3ed991 bd73d13072"]'
            ).get_attribute('innerHTML').split(';')[-1]

  
            collection.append(
                [hotel_name, hotel_price]
            )
            
        return collection
            