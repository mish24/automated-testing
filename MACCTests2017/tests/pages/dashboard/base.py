import re

from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page


class Base(Page):

    _url = '{base_url}/{locale}'

    _amo_logo_locator = (By.CSS_SELECTOR, ".site-title")
    _amo_logo_link_locator = (By.CSS_SELECTOR, ".site-title a")
    _amo_logo_image_locator = (By.CSS_SELECTOR, ".site-title img")

    _footer_locator = (By.CSS_SELECTOR, "#footer")

    def __init__(self, base_url, selenium, locale='en-US', **kwargs):
        super(Base, self).__init__(base_url, selenium, locale=locale, **kwargs)

    def login(self, email, password):
        login_page = self.header.click_login()
        login_page.login(email, password)

    @property
    def page_title(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.selenium.title)
        return self.selenium.title

    @property
    def is_macc_logo_visible(self):
        return self.is_element_visible(*self._macc_logo_locator)

    def click_macc_logo(self):
        self.selenium.find_element(*self._macc_logo_locator).click()
        from pages.dashboard.home import Home
        return Home(self.base_url, self.selenium)

    @property
    def macc_logo_title(self):
        return self.selenium.find_element(*self._macc_logo_link_locator).get_attribute('title')

    @property
    def macc_logo_text(self):
        return self.selenium.find_element(*self._macc_logo_link_locator).text


        @property
        def search_field_placeholder(self):
            return self.selenium.find_element(*self._search_textbox_locator).get_attribute('placeholder')

        @property
        def is_search_button_visible(self):
            return self.is_element_visible(*self._search_button_locator)

        @property
        def is_search_textbox_visible(self):
            return self.is_element_visible(*self._search_textbox_locator)

        @property
        def search_button_title(self):
            return self.selenium.find_element(*self._search_button_locator).get_attribute('title')

        def click_login(self):
            self.selenium.find_element(*self._login_locator).click()
            from pages.dashboard.user import Login
            return Login(self.base_url, self.selenium)

        @property
        def is_login_link_visible(self):
            return self.is_element_visible(*self._login_locator)

        @property
        def is_register_link_visible(self):
            return self.is_element_visible(*self._register_locator)

        def click_logout(self):
            hover_element = self.selenium.find_element(*self._account_controller_locator)
            click_element = self.selenium.find_element(*self._logout_locator)
            ActionChains(self.selenium).move_to_element(hover_element).\
                move_to_element(click_element).\
                click().perform()
            self.wait.until(lambda s: not self.is_user_logged_in)

        def click_edit_profile(self):
            item_locator = (By.CSS_SELECTOR, " li:nth-child(2) a")
            hover_element = self.selenium.find_element(*self._account_controller_locator)
            click_element = self.selenium.find_element(*self._account_dropdown_locator).find_element(*item_locator)
            ActionChains(self.selenium).move_to_element(hover_element).\
                move_to_element(click_element).\
                click().perform()

            from pages.dashboard.user import EditProfile
            return EditProfile(self.base_url, self.selenium)

        def click_view_profile(self):
            item_locator = (By.CSS_SELECTOR, " li:nth-child(1) a")
            hover_element = self.selenium.find_element(*self._account_controller_locator)
            click_element = self.selenium.find_element(*self._account_dropdown_locator).find_element(*item_locator)
            ActionChains(self.selenium).move_to_element(hover_element).\
                move_to_element(click_element).\
                click().perform()


        @property
        def is_user_logged_in(self):
            return self.is_element_visible(*self._account_controller_locator)

        @property
        def menu_name(self):
            return self.selenium.find_element(*self._other_applications_locator).text

        def hover_over_other_apps_menu(self):
            hover_element = self.selenium.find_element(*self._other_applications_locator)
            ActionChains(self.selenium).\
                move_to_element(hover_element).\
                perform()

        @property
        def is_other_apps_dropdown_menu_visible(self):
        return self.selenium.find_element(*self._other_applications_menu_locator).is_displayed()