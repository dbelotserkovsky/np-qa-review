from tir import Webapp
from selenium.webdriver.common.keys import Keys
import tir.technologies.core.enumerations as enum
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By

from datetime import date
import unittest
import time
import sys
import os
from test_ex import Ma3BaseTestClass
# from it_tests.integration_testing_dev.it_hr.it_s30_csa.base_test_class1 import Ma3BaseTestClass

class Atomic(unittest.TestCase, Ma3BaseTestClass):
    @classmethod
    def setUpClass(inst):
        inst.oHelper = Webapp()

    def test_apda010(self):
        self.ac = self.oHelper.GiveMeAccess()

        if self.ac.config.test_type == "s2":
            status_s2 = atomic2_APDA050(self)  # __new__ + __init__

            if status_s2():  # __call__
                print("\nAtomic test s2")
                self.oHelper.AssertTrue()
            else:
                print("\nAtomic test s2")
                self.oHelper.AssertFalse()

        elif self.ac.config.test_type == "smk":
            status_smk = smk_APDA050(self)  # __new__ + __init__

            if status_smk():  # __call__
                print("\nSmoke test")
                self.oHelper.AssertTrue()
            else:
                print("\nSmoke test")
                self.oHelper.AssertFalse()

    @classmethod
    def tearDownClass(inst):
        inst.oHelper.TearDown()


class atomic2_APDA050:
    def __init__(self, mvars):
        self.mvars = mvars

    def __call__(self):
        return self.atomic_APDA050()

    def atomic_APDA050(self):
        self.mvars.oHelper.Setup("SIGACSA", str(date.today().strftime("%d/%m/%Y")), "99", "01", "01")
        self.mvars.oHelper.Program("APDA050")
        self.mvars.menu_routine()
        self.mvars.oHelper.SetButton(self.mvars.oHelper.FindButton("APDA050", "STR0003", "Встав."))
        num = self.mvars.oHelper.GetValue("RDM_CODIGO")
        self.mvars.ac.SaveIndex(
                scenario="apda050_test", descr="RDM_CODIGO", value=num, flag="write"
            )


        self.mvars.oHelper.SetValue("RDM_DESC","КОМАНДА "+ self.mvars.oHelper.GetValue("RDM_CODIGO"))
        team_number = self.mvars.oHelper.GetValue("RDM_DESC")
        self.mvars.ac.SaveIndex(
                scenario="apda050_test", descr="RDM_DESC", value="КОМАНДА "+ self.mvars.oHelper.GetValue("RDM_CODIGO"), flag="write"
            )

        self.mvars.oHelper.SetValue("RD2_DESC", "КУРАТОР КОМАНДЫ", grid_number= 1, row= 1, grid=True)
        self.mvars.oHelper.SetValue("RD2_DESC", "МЛАДШИЙ ТЕСТИРОВШИК", grid_number= 1, row= 2, grid=True)
        self.mvars.oHelper.SetValue("RD2_DESC", "МЛАДШИЙ ТЕСТИРОВШИК", grid_number= 1, row= 3, grid=True)
        self.mvars.oHelper.LoadGrid()

        self.mvars.oHelper.SetButton(self.mvars.ac.language.save)  # Сохранить
        self.mvars.oHelper.SetButton(self.mvars.ac.language.cancel)  # Отмена
        time.sleep(3)
        self.mvars.oHelper.SetButton("Другие Действия", self.mvars.oHelper.FindButton("APDA050", "STR0006", "Создать структуру"))
        time.sleep(3)
        if self.mvars.wait_window('//span[contains(text(), "Компетенции")]',"Компетенции", 10 ): #'//label[contains(text(), "КОМАНДА ТЕСТИРОВШИКОВ")]'
            self.mvars.click_rigt_button(f'//label[contains(text(), "{team_number}")]')
            self.mvars.select_combo_link('//label[contains(text(), "Встав.")]', '//label[contains(text(), "Все позиции списка.")]')
        else:
            print("Окно было не найденно")
        if self.mvars.wait_window('//div/img[@src = "cache/ma3/fwskin_info_ico.png"]', "Информационое окно", 10):
            self.mvars.oHelper.SetButton(self.mvars.ac.language.close) # закрыть
        else:
            pass
        self.mvars.oHelper.SetButton(self.mvars.ac.language.save)  # Сохранить
        return True


class smk_APDA050:
    def __init__(self, mvars):
        self.mvars = mvars

    def __call__(self):
        return self.smoke_run_APDA0500()

    def smoke_run_APDA050(self):
        self.mvars.oHelper.Setup(
            "SIGACSA", str(date.today().strftime("01/%m/%Y")), "00", "102030", "01"
        )
        self.mvars.oHelper.Program("APDA050")
        self.mvars.menu_routine()
        self.mvars.oHelper.SetButton(self.mvars.oHelper.FindButton("APDA050", "STR0003", "Встав."))
        self.mvars.oHelper.SetButton(self.mvars.ac.language.cancel)  # Отмена
        return True





if __name__ == "__main__":
    unittest.main(argv=["ignored-arg"], exit=True)
