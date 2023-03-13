import time

import tir.technologies.core.enumerations as enum
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait


class Ma3BaseTestClass:

    def __init__(self, web_driver):
        self.driver = web_driver
        self.driver.implicitly_wait(10)

    def menu_routine(self):
        count = 0
        while (
            self.ac.element_exists(
                term='//label[contains(text(), "закупк")]',
                scrap_type=enum.ScrapType.XPATH,
            )
            and count < 10
        ):
            count += 1

        ###################### [Docker - menu ma3] ######################
        time.sleep(3)
        try:
            menu_detector = wait(self.ac.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//label[contains(text(), "Найт")]')
                )
            )
        except:
            menu_detector = ""

        if menu_detector:
            print("[INFO] Detected lateral menu on entry point")
            time.sleep(1)
            first_label = '(//li[contains(@style, "fwstd_mnu_01")])[{}]'.format(
                len(
                    self.ac.driver.find_elements(By.XPATH,
                        '//li[contains(@style, "fwstd_mnu_01")]'
                    )
                )
            )
            time.sleep(1)
            self.oHelper.ClickLabel(
                self.ac.driver.find_element(By.XPATH, first_label).text
            )
            time.sleep(1)
            second_label = self.ac.driver.find_element(By.XPATH,
                "(//div[@class=\"tsay twidget transparent dict-tsay align-left\"]/label[contains(text(), '•')])[1]"
            ).text
            time.sleep(1)
            self.oHelper.ClickLabel(second_label)
        else:
            print("[INFO] No lateral menu on entry point")
            pass
    def click_rigt_button(self, loc):
        elm = lambda: self.ac.driver.find_element(By.XPATH, loc)
        elm().click()
        time.sleep(0.5)
        ActionChains(self.ac.driver).context_click(elm()).perform()
        time.sleep(0.5)

    def select_combo_link(self, combbox1, combbox2):
        box1 = lambda: self.ac.driver.find_element(By.XPATH, combbox1)
        box1().click()
        time.sleep(0.5)
        box2 = lambda: self.ac.driver.find_element(By.XPATH, combbox2)
        box2().click()
        time.sleep(0.5)

    def wait_window(self, name_path: str, value_path: str, wait_time: int):
        try:
            button_cbc = lambda: wait(self.ac.driver, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, "{}".format(name_path)))
            )
            button_cbc()
        except:
            button_cbc = ""
        if button_cbc:
            print("[INFO] Label {} found".format(value_path))
            time.sleep(2)
            return button_cbc()
        else:
            print("[ERROR] Label {} not found".format(value_path))
            return False
    def delet_and_select_line(self, loc):
        elm = lambda: self.ac.driver.find_element(By.XPATH, loc)
        elm().click()
        time.sleep(0.5)
        ActionChains(self.ac.driver).send_keys(Keys.DELETE).perform()
        time.sleep(0.5)
        ActionChains(self.ac.driver).send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(2)
        ActionChains(self.ac.driver).send_keys(Keys.F3).perform()

    def xp_double_click(self, loc):
        elm = lambda: self.ac.driver.find_element(By.XPATH, loc)
        time.sleep(1)
        ActionChains(self.ac.driver).double_click(elm()).perform()


    def xp_click_button(self, loc):
        elm = lambda: self.ac.driver.find_element(By.XPATH, loc)
        elm().click()

    def xp_clear_button(self, loc):
        elm = lambda: self.ac.driver.find_element(By.XPATH, loc)
        elm().clear()

    def select_grid_line(self, loc):
        elm = lambda: self.ac.driver.find_element(By.XPATH, loc)
        elm().click()
        time.sleep(0.5)

    def send_num(self, loc,val):
        if self.ac.driver.find_element(By.XPATH, loc).isDispayed() == True:
            try:
                if len(self.ac.driver.find_elements(By.XPATH, loc)) > 0:
                    print("xpath is present")
                    element = lambda: self.ac.driver.find_element(By.XPATH, loc)
                else:
                    print("xpath is not present")
            except:
                pass
        else:
            print("Xpath is not displaed on scrin so it is no exciste")
        element = lambda: self.ac.driver.find_element(By.XPATH, loc)
        time.sleep(4)
        element().send_keys(val, Keys.ENTER)



    def check_valid_db_value(self, db_values, str_to_check, randomex_val):
        existed_values = self.ac.DB_query(db_values)
        flag = False
        for i in existed_values:
            if str_to_check != i[0]:
                continue
            else:
                flag = True
                break
        if flag:
            return self.check_valid_db_value(
                db_values,
                self.oHelper.Randomex(randomex_val),
                randomex_val
                )
        else:
            return str_to_check

    def SearchBySearchBox_1(
        self,
        search_box_name,
        search_by_column=False,
        search_by_key=False
        ):
        import re

        try:
            button = wait(self.ac.driver, 60).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        '//button[contains(@style, "cache/ma3/fwskin_seekbar_ico.png")]',
                    )))
        except:
            print("[ERROR] Filter selection button not found")
        button = lambda: self.ac.driver.find_element(By.XPATH,
            '//button[contains(@style, "cache/ma3/fwskin_seekbar_ico.png")]'

        )
        time.sleep(1)
        button().click()
        time.sleep(1)

        if search_by_column != False:
            path_label = f'//a[contains(text(), "{search_box_name}")]'
            label = lambda: self.ac.driver.find_element(By.XPATH, path_label)
            time.sleep(1)
            label().click()
            time.sleep(2)
            if re.match("[0-9]+$", search_by_column):
                path_column = f'(//label[contains(@class, "tcheckbox twidget dict-tcheckbox")]/input)[{search_by_column}]'
            else:
                path_column = f'//span[contains(text(), "{search_by_column}")]'

            column = lambda: self.ac.driver.find_element(By.XPATH, path_column)
            time.sleep(1)
            column().click()
            time.sleep(1)

        elif search_by_key != False:
            pass
    def select_type_scale(self):
        ActionChains(self.ac.driver).send_keys(Keys.SPACE).perform()
        time.sleep(0.5)
        ActionChains(self.ac.driver).send_keys(Keys.ARROW_UP).perform()
        time.sleep(0.5)
        # счечм=ик сделать
        ActionChains(self.ac.driver).send_keys(Keys.ARROW_UP).perform()
        time.sleep(0.5)
        ActionChains(self.ac.driver).send_keys(Keys.ENTER).perform()
        time.sleep(0.5)

    def select_importance_level(self):
        ActionChains(self.ac.driver).send_keys(Keys.SPACE).perform()
        time.sleep(0.5)
        ActionChains(self.ac.driver).send_keys(Keys.ARROW_UP).perform()
        time.sleep(0.5)
        ActionChains(self.ac.driver).send_keys(Keys.ENTER).perform()
        time.sleep(0.5)

    def select_skill(self):
        ActionChains(self.ac.driver).send_keys(Keys.DELETE).perform()
        time.sleep(1)
        ActionChains(self.ac.driver).send_keys(Keys.ARROW_RIGHT).perform()
        time.sleep(1)
        ActionChains(self.ac.driver).send_keys(Keys.ENTER).perform()

    def select_value(self, value_1: str, value_2: str):
        time.sleep(1)
        element= self.ac.driver.find_element(By.XPATH, f'(//select)[{value_1}]')
        element.click()
        for option in element.find_elements(By.TAG_NAME, "option"):
            if option.text == value_2:
                option.click()
                break
        time.sleep(1)
        print(f"[INFO] Parameter {value_2} was set")

    def find_element_in_grid(self, loc):
        while self.waiter(loc) != True:
            ActionChains(self.ac.driver).send_keys(Keys.PAGE_DOWN).perform()

    def find_element_in_grid_click(self, loc):
        while self.waiter(loc) != True:
            ActionChains(self.ac.driver).send_keys(Keys.PAGE_DOWN).perform()
        elm = lambda: self.ac.driver.find_element(By.XPATH, loc)
        elm().click()
        time.sleep(0.5)



    def waiter(self, xpath_elem: str):
        time.sleep(1)
        try:
            detect_something = wait(self.ac.driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, xpath_elem))
            )
        except:
            detect_something = ""
        if detect_something:
            print(f"\n[INFO] window with element {xpath_elem} was found")
            return True
        else:
            print(f"\n[INFO]window with element {xpath_elem} not found")
            return False
