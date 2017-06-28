import pytest


from pages.dashboard.home import Home


class TestDashboardLayout:

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_dashboard_for_users(self, base_url, selenium):
        app_under_test = "infohub"
        home_page = Home(base_url, selenium)
        home_page.header.click_other_application(app_under_test)
        assert app_under_test.lower() in home_page.get_url_current_page()
        assert not home_page.header.is_other_application_visible(app_under_test)

    @pytest.mark.nondestructive
    def test_that_checks_macc_logo_text_layout_and_title(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        assert 'Mobile App Control Center' == home_page.macc_logo_text
        assert 'Mobile App Control Center' == home_page.macc_logo_title

    @pytest.mark.nondestructive
    def test_that_clicking_the_macc_logo_loads_home_page(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        assert home_page.is_macc_logo_visible
        home_page = home_page.click_macc_logo()
        assert home_page.is_the_current_page
        assert home_page.is_macc_logo_visible
        assert'%s/en-US/firefox/' % home_page.base_url == home_page.get_url_current_page()


    @pytest.mark.nondestructive
    def test_the_search_field_placeholder(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        assert 'Welcome, User' == home_page.header.search_field_placeholder
        assert home_page.header.is_search_button_visible
        assert 'Logout' == home_page.header.search_button_title

    @pytest.mark.nondestructive
    def test_the_search_box_exist(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        assert home_page.header.is_search_logout_button_visible
