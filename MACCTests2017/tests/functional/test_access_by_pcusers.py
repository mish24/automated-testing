import datetime
import pytest


from django.core.management import call_command
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pcsa.models import PcsaPost
from signup.models import Pcuser

pytestmark = pytest.mark.selenium

@pytest.fixture
def initial_data(transactional_db):
	call_command('load_initial_data')

def test_pcsa_dashboard(initial_data, live_server, selenium):
	"""
	Tests that the default pcsa dashboard page laods okay
	and we can click the required links
	"""
	selenium.get(live_server.url + '/')
	logo_button = WebDriverWait(selenium, 20).until(
		EC.presence_of_element_located(By.ID, 'dashboard'))
	
	logo_button.click()
	assert selenium.find_element_by_id('logo_button').is_displayed()


def test_pcsa_header(initial_data, live_server, selenium):
	"""
	This tests that the basic features of the dashboard header
	are displayed properly and all the necessary buttons are present
	"""
	selenium.get(live_server.url)
	first_name = WebDriverWait(selenium, 20).until(
		EC.presence_of_element_located(By.ID, first_name))
	first_name.click()
	WebDriverWait(selenium, 20).until(
		EC.presence_of_element_located(By.ID, 'dashboard'))

