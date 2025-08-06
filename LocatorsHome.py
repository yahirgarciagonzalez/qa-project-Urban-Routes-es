import data
from methods import confirmation_code
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LocatorsHome:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        driver.maximize_window()


        self.from_input = (By.ID, "from")
        self.to_input = (By.ID, "to")
        self.personal_mode = (By.CSS_SELECTOR, ".modes-container > div:nth-child(3)")
        self.personal_taxi = (By.CSS_SELECTOR, ".types-container > div:nth-child(3) > img")
        self.request_taxi_button = (By.CSS_SELECTOR, ".results-text > button")
        self.comfort_rate = (By.CSS_SELECTOR, ".tariff-cards > div:nth-child(5) > div.tcard-icon > img")
        self.phone_input = (By.CSS_SELECTOR, ".tariff-picker.shown > div.form > div.np-button > div")
        self.phone_field = (By.ID, "phone")
        self.next_button = (By.CSS_SELECTOR, ".buttons > button")
        self.code_input = (By.CSS_SELECTOR, ".np-input > div.input-container")
        self.code_field = (By.ID, "code")
        self.confirm_button = (By.XPATH, "//button[text()='Confirmar']")
        self.card_payment_method = (By.CSS_SELECTOR, ".pp-button")
        self.card_option = (By.CSS_SELECTOR, ".payment-picker.open .pp-selector .pp-row.disabled .pp-title")
        self.card_number_input = (By.ID, "number")
        self.card_code_cvc_input = (By.XPATH, "//input[@placeholder='12']")
        self.add_card = (By.CSS_SELECTOR, ".payment-picker.open .modal .section.active")
        self.link_card_button = (By.CSS_SELECTOR, ".pp-buttons > button:nth-child(1)")
        self.close_button = (By.CSS_SELECTOR, '.payment-picker .close-button')
        self.pp_value = (By.CLASS_NAME, "pp-value-text")
        self.driver_message_input = (By.ID, "comment")
        self.blanket_and_tissues = (By.CSS_SELECTOR, ".reqs-body > div:nth-child(1) > div > div.r-sw > div > span")
        self.ice_cream_add_button = (By.CSS_SELECTOR, ".r-group-items > div:nth-child(1) > div > div.r-counter > div > div.counter-plus")
        self.ice_cream_counter = (By.CSS_SELECTOR, ".counter-value")
        self.submit_button = (By.CSS_SELECTOR, ".smart-button-wrapper > button")
        self.taxi_finder = (By.CSS_SELECTOR, ".order.shown > div.order-body")
        self.driver_details = (By.CSS_SELECTOR, ".order-subbody > div.order-buttons > div:nth-child(1) > div.order-button > img")


    def enter_addresses(self, from_address, to_address):
        from_container = self.wait.until(EC.presence_of_element_located(self.from_input))
        from_container.send_keys(from_address)
        to_container = self.wait.until(EC.presence_of_element_located(self.to_input))
        to_container.send_keys(to_address)

    def get_from_input_value(self):
        return self.driver.find_element(*self.from_input).get_attribute("value")

    def get_to_input_value(self):
        return self.driver.find_element(*self.to_input).get_attribute("value")

    def select_comfort_tariff(self):
        self.wait.until(EC.element_to_be_clickable(self.personal_mode)).click()
        self.wait.until(EC.element_to_be_clickable(self.personal_taxi)).click()
        self.wait.until(EC.element_to_be_clickable(self.request_taxi_button)).click()

        comfort_option = self.wait.until(EC.presence_of_element_located(self.comfort_rate))

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comfort_option)
        self.wait.until(EC.element_to_be_clickable(self.comfort_rate)).click()

    def comfort_tariff_selected(self):
        tariffs = self.driver.find_elements(By.CLASS_NAME, "tcard")
        for tariff in tariffs:
            if "Comfort" in tariff.text and "active" in tariff.get_attribute("class"):
                return True

    def enter_phone_number(self):
        WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(self.phone_input)).click()
        WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(self.phone_field)).send_keys(data.phone_number)
        self.driver.find_element(*self.next_button).click()

        phone_code_helper = confirmation_code(self.driver)
        code = phone_code_helper.retrieve_phone_code(self.driver)

        WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(self.code_field))
        self.driver.find_element(*self.code_field).send_keys(code)
        self.driver.find_element(*self.confirm_button).click()

    def phone_input_filled_correctly(self):
        return self.driver.find_element(*self.phone_field).get_property('value')

    def add_credit_card(self, number, cvc):

            WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(self.card_payment_method)).click()
            WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(self.card_option)).click()
            self.wait.until(EC.visibility_of_element_located(self.card_number_input)).send_keys(number)
            self.wait.until(EC.visibility_of_element_located(self.card_code_cvc_input)).send_keys(cvc)

            WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(self.add_card)).click()
            self.wait.until(EC.element_to_be_clickable(self.link_card_button)).click()
            WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(self.close_button)).click()

    def is_card_linked(self):
        return self.driver.find_element(*self.pp_value).text

    def write_driver_message(self, message):
        message_box = self.wait.until(EC.presence_of_element_located(self.driver_message_input))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", message_box)
        message_box.clear()
        message_box.send_keys(message)

    def message_sent(self, expected_message):
        driver_message_input = self.driver.find_element(*self.driver_message_input)
        return expected_message in driver_message_input.get_attribute("value")

    def activate_blanket_and_tissues(self):
        option = self.wait.until(EC.element_to_be_clickable(self.blanket_and_tissues))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
        option.click()

    def blanket_and_tissues_selected(self):
        checkbox = self.driver.find_element(By.CSS_SELECTOR, "input.switch-input")
        return checkbox.is_selected()

    def add_ice_cream(self, quantity=2):
        button = self.wait.until(EC.element_to_be_clickable(self.ice_cream_add_button))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        for _ in range(quantity):
            button.click()
            self.wait.until(EC.element_to_be_clickable(self.ice_cream_add_button))

    def get_ice_cream_count(self):
        counter = self.driver.find_element(*self.ice_cream_counter)
        return int(counter.text.strip())

    def ice_cream_add(self):
        return self.get_ice_cream_count() == 2

    def confirm_trip(self):
        button = self.wait.until(EC.presence_of_element_located(self.submit_button))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        self.wait.until(EC.element_to_be_clickable(self.submit_button)).click()

    def taxi_modal(self, timeout=5):
        driver_img = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(self.taxi_finder))
        return driver_img.is_displayed()

    def wait_for_driver_details(self, timeout=10):
        driver_img = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(self.driver_details))
        return driver_img.is_displayed()