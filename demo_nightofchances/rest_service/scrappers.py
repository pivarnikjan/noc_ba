import os
from time import sleep

import logging

import django
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def set_django_env():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_nightofchances.settings')
    django.setup()

set_django_env()
from rest_service.models import Hotels

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT)


class HotelsScrapping(object):
    _hotel_url = "https://sk.hotels.com/"

    # LOCATORS:
    _destination = "qf-0q-destination"
    _check_in = "qf-0q-localised-check-in"
    _check_out = "qf-0q-localised-check-out"
    _search = "//button[@type='submit']"

    _sorting = "//ul[@id='enhanced-sort']/li[5]"
    _ascending_order = "//ul[@id='enhanced-sort']//a[@data-option-id='opt_PRICE']"
    _lowest_price = "//div[@id='listings']/ol/li[1]//ins|//div[@id='listings']/ol/li[1]//div[@class='price']//b"

    _list_of_hotel_names = "//div[@id='listings']//article//h3//a"
    _list_of_hotel_addresses = "//div[@id='listings']//article//div[@class='contact']//span[@class='p-street-address']"
    _list_of_hotel_localities = "//div[@id='listings']//article//div[@class='contact']//span[@class='p-locality']"
    _list_of_hotel_postal_codes = "//div[@id='listings']//article//div[@class='contact']//span[@class='p-postal-code']"
    _list_of_hotel_country_names = "//div[@id='listings']//article//div[@class='contact']//span[@class='p-country-name']"
    _list_of_ratings = "//div[@id='listings']//article//span[@class='guest-rating-value']/strong"
    _list_of_prices = "//div[@id='listings']//div[@class='price']//b|//div[@id='listings']/ol//ins"
    _list_of_images = "//div[@id='listings']//a/img"

    def __init__(self, driver, city, check_in_date='2018-3-14', check_out_date='2018-3-18'):
        self.driver = driver
        self.driver.set_window_size(1600, 900)
        self.driver.implicitly_wait(2)

        self.city = city
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date

        self._check_in_date = "//td[@data-date='{}']".format(check_in_date)
        self._check_out_date = "//td[@data-date='{}']".format(check_out_date)

    def fill_destination_form(self):
        _logger.info('{} Filling form {}'.format(15*'*', 15*'*'))

        check_in = self.driver.find_element(By.ID, self._check_in)
        _logger.debug('check_in {}'.format(check_in))
        check_in.click()
        check_in_date = self.driver.find_element(By.XPATH, self._check_in_date)
        _logger.debug('check_in_date {}'.format(check_in_date))
        check_in_date.click()

        check_out = self.driver.find_element(By.ID, self._check_out)
        _logger.debug('check_out {}'.format(check_out))
        check_out.click()
        check_out_date = self.driver.find_element(By.XPATH, self._check_out_date)
        _logger.debug('check_out_date {}'.format(check_out_date))
        check_out_date.click()

        destination = self.driver.find_element(By.ID, self._destination)
        _logger.debug('destination {}'.format(destination))
        destination.send_keys(self.city)
        destination.send_keys(Keys.ENTER)

    def apply_filter(self):
        sleep(9)
        _logger.info('{} Applying filter {}'.format(15*'*', 15*'*'))
        element_to_hover_over = self.driver.find_element(By.XPATH, self._sorting)
        _logger.debug('element_to_hover_over {}'.format(element_to_hover_over))

        element_to_click_on = self.driver.find_element(By.XPATH, self._ascending_order)
        _logger.debug('element_to_click_on {}'.format(element_to_click_on))

        hover = ActionChains(self.driver).move_to_element(element_to_hover_over).move_to_element(element_to_click_on)
        _logger.debug('hover {}'.format(hover))
        hover.click().perform()
        sleep(5)

    def init_step(self):
        self.driver.get(self._hotel_url)
        self.fill_destination_form()
        self.apply_filter()

    def get_lowest_price(self):
        self.init_step()

        _logger.info('{} Getting lowest price {}'.format(15*'*', 15*'*'))
        price = self.driver.find_element(By.XPATH, self._lowest_price)
        _logger.debug('price {}'.format(price))
        price = int(price.text[:-1])
        self.driver.quit()
        return price

    def _get_elements(self, locator, by_type=By.XPATH):
        return self.driver.find_elements(by_type, locator)

    @staticmethod
    def _get_text_from_elements(elements):
        return [el.text for el in elements]

    def get_list_of_cheapest_hotels(self):
        names_el = self._get_elements(self._list_of_hotel_names)
        names = self._get_text_from_elements(names_el)

        addresses_el = self._get_elements(self._list_of_hotel_addresses)
        addresses = self._get_text_from_elements(addresses_el)

        localities_el = self._get_elements(self._list_of_hotel_localities)
        localities = [el.text[2:] for el in localities_el]

        postal_codes_el = self._get_elements(self._list_of_hotel_postal_codes)
        postal_codes = [el.text[2:] for el in postal_codes_el]

        country_names_el = self._get_elements(self._list_of_hotel_country_names)
        country_names = self._get_text_from_elements(country_names_el)

        ratings_el = self._get_elements(self._list_of_ratings)
        ratings = self._get_text_from_elements(ratings_el)

        prices_el = self._get_elements(self._list_of_prices)
        prices = self._get_text_from_elements(prices_el)

        images_el = self._get_elements(self._list_of_images)
        images = [url.get_attribute('style')[23:-3] for url in images_el]  # parsing out background-image: url ("");

        list_of_cheapest_hotels = zip(names, addresses, localities, postal_codes, country_names, ratings, prices, images)
        return list_of_cheapest_hotels

    def get_cheapest_hotels_detail(self):
        self.init_step()
        sleep(2)

        _logger.info('{} Scrolling down page {}'.format(15 * '*', 15 * '*'))
        self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        sleep(3)

        hotels = self.get_list_of_cheapest_hotels()
        self.store_hotels_detail(hotels)
        self.driver.quit()
        return hotels

    @staticmethod
    def _get_fields_names():
        meta_fields = Hotels._meta.get_fields()
        names = [field.name for field in meta_fields]
        return names[1:-2]

    def _clean_hotels_detail(self):
        queryset = Hotels.objects.filter(city=self.city)
        if queryset:
            queryset.delete()

    def store_hotels_detail(self, list_of_cheapest_hotels):
        bulk_list = []
        fields_names = self._get_fields_names()

        self._clean_hotels_detail()

        for hotel in list_of_cheapest_hotels:
            f = Hotels()
            for idx, field in enumerate(fields_names):
                if field == 'city':
                    setattr(f, 'city', self.city)
                    setattr(f, 'check_in_date', self.check_in_date)
                    setattr(f, 'check_out_date', self.check_out_date)
                else:
                    setattr(f, field, hotel[idx])
            bulk_list.append(f)
        Hotels.objects.bulk_create(bulk_list)


class TestingPhantomJS(object):
    def __init__(self, driver):
        self.driver = driver
        self.driver.set_window_size(1600, 900)

    def print_page_source(self):
        self.driver.get('https://www.hotels.com')
        print(self.driver.page_source)
        self.driver.quit()


def test():

    driver = webdriver.PhantomJS()
    tmp = TestingPhantomJS(driver)
    tmp.print_page_source()


def main():
    driver = webdriver.Firefox()
    ss = HotelsScrapping(driver, 'Amsterdam')

    ss.get_cheapest_hotels_detail()
    # tmp = ss.get_lowest_price()
    # if tmp < 170:
    #     print("Je cas nakupovat")
    # else:
    #     print("Cena je prilis velka")


if __name__ == '__main__':
    main()
