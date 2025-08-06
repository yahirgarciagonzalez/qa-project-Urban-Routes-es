import data
from LocatorsHome import LocatorsHome
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from data import urban_routes_url
from data import card_number, card_code
from data import message_for_driver
from data import address_from, address_to

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("perfLoggingPrefs", {'enableNetwork': True, 'enablePage': True})
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.get(urban_routes_url)
        cls.home = LocatorsHome(cls.driver)

    def test01_enter_addresses(self):
        self.home.enter_addresses(address_from, address_to)

        assert self.home.get_from_input_value() == address_from
        assert self.home.get_to_input_value() == address_to

    def test02_select_comfort_tariff(self):
        self.home.select_comfort_tariff()

        assert self.home.comfort_tariff_selected(), "No se seleccionó la tarifa Comfort"

    def test03_enter_phone_number(self):
        self.home.enter_phone_number()
        actual_number = data.phone_number
        phone_number_written = self.home.phone_input_filled_correctly()

        assert phone_number_written == actual_number
        WebDriverWait(self.driver, timeout=3)

    def test04_add_credit_card(self):
        self.home.add_credit_card(card_number, card_code)

        assert self.home.is_card_linked(), "La tarjeta no se agregó"

    def test05_write_driver_message(self):
        self.home.write_driver_message(message_for_driver)

        assert self.home.message_sent(message_for_driver), "No se ingresó correctamente el mensaje al conductor"

    def test06_activate_blanket_and_tissues(self):
        self.home.activate_blanket_and_tissues()

        assert self.home.blanket_and_tissues_selected(), "No se seleccionó la opción de manta y pañuelos"

    def test07_add_ice_cream(self):
        self.home.add_ice_cream()

        assert self.home.ice_cream_add(), "No se agregaron los 2 helados"

    def test08_taxi_seeker_appears(self):
        self.home.confirm_trip()

        assert self.home.taxi_modal(), "No se visualiza la ventana buscar taxi"

    def test09_confirm_trip_check_driver(self):
        assert self.home.wait_for_driver_details(), "Los detalles del conductor no se visualizan"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
