from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page
from pages.desktop.base import Base


class Home(Base):

    _page_title = "Mobile App Control Center"
    _first_addon_locator = (By.CSS_SELECTOR, ".summary > a > h3")
    _other_applications_link_locator = (By.ID, "other-apps")

    # Most Popular List
    _most_popular_item_locator = (By.CSS_SELECTOR, "ol.toplist li")
    _most_popular_list_heading_locator = (By.CSS_SELECTOR, "#homepage > .secondary h2")

    _explore_side_navigation_header_locator = (By.CSS_SELECTOR, "#side-nav > h2:nth-child(1)")
    _explore_featured_link_locator = (By.CSS_SELECTOR, "#side-nav .s-featured a")
    _explore_popular_link_locator = (By.CSS_SELECTOR, "#side-nav .s-users a")
    _explore_top_rated_link_locator = (By.CSS_SELECTOR, "#side-nav .s-rating a")

    _featured_themes_see_all_link = (By.CSS_SELECTOR, "#featured-themes h2 a")
    _featured_themes_title_locator = (By.CSS_SELECTOR, "#featured-themes h2")
    _featured_themes_items_locator = (By.CSS_SELECTOR, "#featured-themes li")

    _featured_collections_locator = (By.CSS_SELECTOR, "#featured-collections h2")
    _featured_collections_elements_locator = (By.CSS_SELECTOR, "#featured-collections section:nth-child(1) li")

    _featured_extensions_title_locator = (By.CSS_SELECTOR, '#featured-extensions > h2')
    _featured_extensions_see_all_locator = (By.CSS_SELECTOR, '#featured-extensions > h2 > a')
    _featured_extensions_elements_locator = (By.CSS_SELECTOR, '#featured-extensions section:nth-child(1) > li > div')

    _extensions_menu_link = (By.CSS_SELECTOR, "#extensions > a")

    _promo_box_locator = (By.ID, "promos")

    _up_and_coming_locator = (By.ID, 'upandcoming')

    def __init__(self, base_url, selenium, open_url=True):
        """Creates a new instance of the class and gets the page ready for testing."""
        Base.__init__(self, base_url, selenium)
        if open_url:
            self.selenium.get(self.base_url)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: s.find_element(*self._promo_box_locator).size['height'] == 271)

    def macc_home_title(self):
        home_item = self.selenium.find_element(*self._macc_logo_link_locator)
        ActionChains(self.selenium).\
            move_to_element(home_item).\
            perform()

    def click_featured_themes_see_all_link(self):
        self.selenium.find_element(*self._featured_themes_see_all_link).click()
        from pages.desktop.themes import Themes
        return Themes(self.base_url, self.selenium)

    def click_featured_collections_see_all_link(self):
        self.selenium.find_element(*self._featured_collections_locator).find_element(By.CSS_SELECTOR, " a").click()
        from pages.desktop.collections import Collections
        return Collections(self.base_url, self.selenium)

    def click_to_explore(self, what):
        what = what.replace(' ', '_').lower()
        self.selenium.find_element(*getattr(self, "_explore_%s_link_locator" % what)).click()
        from pages.desktop.extensions import ExtensionsHome
        return ExtensionsHome(self.base_url, self.selenium)

    def get_category(self):
        from pages.desktop.category import Category
        return Category(self.base_url, self.selenium)

    def get_title_of_link(self, name):
        name = name.lower().replace(" ", "_")
        locator = getattr(self, "_%s_link_locator" % name)
        return self.selenium.find_element(*locator).get_attribute('title')


 
