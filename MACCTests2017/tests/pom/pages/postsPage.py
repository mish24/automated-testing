from basePage import *
from pom.locators.eventsPageLocators import *
from selenium.webdriver.support.ui import Select
from pom.pages.homePage import HomePage
from pom.pageUrls import PageUrls

class EventsPage(BasePage):

    event_list_page = PageUrls.event_list_page
    pcsa_post_list_page = PageUrls.pcsa_post_list_page
    malaria_post_list_page = PageUrls.malaria_post_list_page
    pcsapost_tab = 'PcsaPost'
    malaria_post_tab = 'MalariaPost'
    live_server_url = ''

    def __init__(self, driver):
        self.driver = driver
        self.home_page = HomePage(self.driver)
        self.elements = EventsPageLocators()
        super(EventsPage, self).__init__(driver)

    def fill_pcsa_post_form(self, event):
        self.element_by_xpath(self.elements.CREATE_PCSAPOST_NAME).clear()
        self.element_by_xpath(self.elements.CREATE_PCSAPOST_START_DATE).clear()
        self.element_by_xpath(self.elements.CREATE_PCSAPOST_END_DATE).clear()
        self.send_value_to_xpath(self.elements.CREATE_PCSAPOST_NAME, event[0])
        self.send_value_to_xpath(self.elements.CREATE_PCSAPOST_START_DATE, event[1])
        self.send_value_to_xpath(self.elements.CREATE_PCSAPOST_END_DATE, event[2])
        self.submit_form()

    def fill_malaria_post_form(self, job):
        self.element_by_xpath(self.elements.CREATE_MALARIAPOST_NAME).clear()
        self.element_by_xpath(self.elements.CREATE_MALARIAPOST_DESCRIPTION).clear()
        self.element_by_xpath(self.elements.CREATE_MALARIAPOST_START_DATE).clear()
        self.element_by_xpath(self.elements.CREATE_MALARIAPOST_END_DATE).clear()

        self.send_value_to_xpath(self.elements.CREATE_MALARIAPOST_ID,job[0])
        self.send_value_to_xpath(self.elements.CREATE_MALARIAPOST_NAME,job[1])
        self.send_value_to_xpath(self.elements.CREATE_MALARIAPOST_DESCRIPTION,job[2])
        self.send_value_to_xpath(self.elements.CREATE_MALARIAPOST_START_DATE,job[3])
        self.send_value_to_xpath(self.elements.CREATE_MALARIAPOST_END_DATE,job[4])
        self.submit_form()


    def submit_form(self):
        self.element_by_xpath(self.elements.GENERAL_SUBMIT_PATH).submit()

    def go_to_pcsa_posts_list_page(self):
        self.home_page.get_events_link().send_keys('\n')

    def navigate_to_pcsa_post_list_view(self):
        self.get_page(self.live_server_url, self.pcsa_post_list_page)

    def navigate_to_malaria_post_list_view(self):
        self.get_page(self.live_server_url, self.malaria_post_list_page)

    def go_to_create_pcsapost_page(self):
        self.click_link('Create PCSA Post')

    def go_to_edit_pcsapost_page(self):
        self.element_by_xpath(self.elements.EDIT_PCSAPOST).click()

    def go_to_delete_pcsapost_page(self):
        self.get_page(self.live_server_url, self.create_PCSAPOST_page)

    def go_to_create_malaria_posts_page(self):
        self.click_link('Create Malaria Post')

    def go_to_edit_malaria_posts_page(self):
        self.element_by_xpath(self.elements.EDIT_MALARIAPOST.click()

    def go_to_delete_malaria_posts_page(self):
        self.get_page(self.live_server_url, self.delete_malaria_posts_page)

    def get_deletion_box(self):
        return self.element_by_class_name(self.elements.DELETION_BOX)

    def get_deletion_context(self):
        return self.element_by_class_name(self.elements.DELETION_POST).text

    def get_message_context(self):
        return self.element_by_class_name(self.elements.MESSAGE_BOX).text

    def get_warning_context(self):
        return self.element_by_class_name(self.elements.WARNING_CONTEXT).text

    def get_danger_message(self):
        return self.element_by_class_name(self.elements.DANGER_BOX)

    def get_template_error_message(self):
        return self.element_by_xpath(self.elements.TEMPLATE_ERROR_MESSAGE).text

    def get_results(self):
        return self.element_by_xpath(self.elements.RESULTS)

    def get_pcsa_post_date(self):
        return self.element_by_xpath(self.elements.PCSAPOST).text

    def get_help_block(self):
        return self.element_by_class_name(self.elements.HELP_BLOCK)

    def get_help_blocks(self):
	return self.elements_by_class_name(self.elements.HELP_BLOCKS)
