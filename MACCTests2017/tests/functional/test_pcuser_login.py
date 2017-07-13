from django.contrib.staticfiles.testing import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from pom.pages.authenticationPage import AuthenticationPage
from pom.pageUrls import PageUrls

from shift.utils import (
    create_admin,
    create_pcuser
    )

import re

class TestAccessControl(LiveServerTestCase):
    '''
    TestAccessControl class contains the functional tests to check Admin and
    Pcuser can access '/home' view of MACC. Following tests are included:
    Administrator:
        - Login admin with correct credentials
        - Login admin with incorrect credentials 
    Pcuser:
        - Login pcuser with correct credentials
        - Login pcuser with incorrect credentials 
    '''
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        cls.authentication_page = AuthenticationPage(cls.driver)
        super(TestAccessControl, cls).setUpClass()

    def setUp(self):
        admin = create_admin()
        volunteer = create_pcuser()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(TestAccessControl, cls).tearDownClass()

    def test_correct_admin_credentials(self):
        '''
        Method to simulate logging in of a valid admin user and check if they
        redirected to '/home' and no errors are generated.
        '''
        authentication_page = self.authentication_page
        self.authentication_page.server_url = self.live_server_url
        authentication_page.login({ 'username' : 'admin', 'password' : 'admin'})
        self.assertEqual(self.driver.current_url, self.live_server_url +
                authentication_page.homepage)

        with self.assertRaises(NoSuchElementException):
            authentication_page.get_incorrect_login_message()
        authentication_page.logout()

    def test_incorrect_admin_credentials(self):
        '''
        Method to simulate logging in of an Invalid admin user and check if
        they are displayed an error and redirected to login page again.
        '''
        authentication_page = self.authentication_page
        self.authentication_page.server_url = self.live_server_url
        authentication_page.login({ 'username' : 'admin', 'password' : 'wrong_password'})
        self.assertNotEqual(self.driver.current_url, self.live_server_url +
                authentication_page.homepage)

        self.assertEqual(self.driver.current_url, self.live_server_url +
                authentication_page.url)

        self.assertNotEqual(authentication_page.get_incorrect_login_message(), None)

    def test_correct_pcuser_credentials(self):
        '''
        Method to simulate logging in of a valid pcuser and check if
        they are redirected to '/home'
        '''
        authentication_page = self.authentication_page
        self.authentication_page.server_url = self.live_server_url
        authentication_page.login({ 'username' : 'mish24', 'password' : 'password'})
        self.assertEqual(self.driver.current_url, self.live_server_url +
                authentication_page.homepage)

        with self.assertRaises(NoSuchElementException):
            authentication_page.get_incorrect_login_message()
        authentication_page.logout()

    def test_incorrect_pcuser_credentials(self):
        '''
        Method to simulate logging in of a Invalid volunteer user and check if
        they are displayed an error and redirected to login page again.
        '''
        authentication_page = self.authentication_page
        self.authentication_page.server_url = self.live_server_url
        authentication_page.login({ 'username' : 'mish24', 'password' : 'wrong_password'})
        
        self.assertNotEqual(self.driver.current_url, self.live_server_url +
                authentication_page.homepage)

        self.assertEqual(self.driver.current_url, self.live_server_url +
                authentication_page.url)

	self.assertNotEqual(authentication_page.get_incorrect_login_message(), None)
