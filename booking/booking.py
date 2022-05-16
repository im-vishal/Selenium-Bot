from lib2to3.pgen2 import driver
import booking.constants as const
from selenium.webdriver.common.by import By
import os
from selenium import webdriver
from booking.booking_filteration import BookingFilteration
from booking.booking_export import BookingExport
import warnings
from prettytable import PrettyTable

warnings.filterwarnings("ignore", category=DeprecationWarning)


class Booking(webdriver.Chrome):
    def __init__(self, driver_path= r"C:\SeleniumDrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=option)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, *args):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

  
    def change_currency(self, currency= None):
        currency_element = self.find_element_by_css_selector(
            'button[data-tooltip-text="Choose your currency"]'
        )
        currency_element.click()

        selected_currency = self.find_element_by_css_selector(
            f'a[data-modal-header-async-url-param*="selected_currency={currency}"]'
        )
        selected_currency.click()

    def select_places_to_go(self, place_to_go):
        search_field = self.find_element_by_id('ss')
        search_field.clear()
        search_field.send_keys(place_to_go)

        first_result = self.find_element_by_css_selector(
            'li[data-i="0"]'
        )
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element_by_css_selector(
            f'td[data-date="{check_in_date}"]'
        )
        check_in_element.click()

        check_out_element = self.find_element_by_css_selector(
            f'td[data-date="{check_out_date}"]'
        )
        check_out_element.click()

    def select_adults(self, count=1):
        selection_element = self.find_element_by_id('xp__guests__toggle')
        selection_element.click()


        decrease_adults_element = self.find_element_by_css_selector(
            'button[aria-label="Decrease number of Adults"]'
        )

        while True:
            decrease_adults_element.click()
            # if the value of adults reaches 1, then we should get out of the loop
            adults_value_element = self.find_element_by_id('group_adults')
            adults_value = adults_value_element.get_attribute(
                'value') # will give the adult count

            if int(adults_value) == 1:
                break

        increase_adults_element = self.find_element_by_css_selector(
            'button[aria-label="Increase number of Adults"]'
        )
        
        for _ in range(count - 1):
            increase_adults_element.click()

    def click_search(self):
        self.find_element_by_css_selector(
            'button[type="submit"]'
        ).click()

    def apply_filterations(self):
        filteration = BookingFilteration(driver=self)
        filteration.apply_star_rating(3, 4, 5)
        filteration.sort_price_lowest_fist()

    def export_results(self):
        hotel_boxes = self.find_element(By.ID, 'search_results_table'
        )

        export = BookingExport(hotel_boxes)
        table = PrettyTable(
            field_names=['Hotel Name', 'Hotel Price']
        )
        table.add_rows(export.pull_deal_box_attributes())
        print(table)

   