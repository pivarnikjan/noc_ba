import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rest_service.scrappers import HotelsScrapping


class TestLocators(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        driver = webdriver.PhantomJS()
        cls.ss = HotelsScrapping(driver, city='Amsterdam')
        cls.ss.driver.get(cls.ss._hotel_url)

    def is_element_present(self, how, what):
        try:
            elem = WebDriverWait(self.ss.driver, 10).until(EC.presence_of_element_located((how, what)))
            # elem = self.ss.driver.find_element(by=how, value=what)
        except NoSuchElementException:
            return False, None
        return True, elem

    def test_check_in_locator(self):
        presence, el = self.is_element_present(By.ID, self.ss._check_in)
        self.assertTrue(presence)
        el.click()

        presence, el_date = self.is_element_present(By.XPATH, self.ss._check_in_date)
        self.assertTrue(presence)

    def test_check_out_locator(self):
        presence, el = self.is_element_present(By.ID, self.ss._check_out)
        self.assertTrue(presence)
        el.click()

        presence, el_date = self.is_element_present(By.XPATH, self.ss._check_out_date)
        self.assertTrue(presence)

    def test_destination_locator(self):
        presence, el = self.is_element_present(By.ID, self.ss._destination)
        self.assertTrue(presence)
        el.send_keys(self.ss.city)
        el.send_keys(Keys.ENTER)

    def test_processed_page(self):
        presence, el_sort = self.is_element_present(By.XPATH, self.ss._sorting)
        self.assertTrue(presence)

        presence, el_asc = self.is_element_present(By.XPATH, self.ss._ascending_order)
        self.assertTrue(presence)

    @classmethod
    def tearDownClass(cls):
        cls.ss.driver.quit()


if __name__ == '__main__':
    unittest.main()
