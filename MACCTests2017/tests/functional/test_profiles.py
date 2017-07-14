from django.contrib.staticfiles.testing import LiveServerTestCase

from pom.pages.authenticationPage import AuthenticationPage
from pom.locators.pcsaPageLocators import *

from pcsa.models import pcsaPosts
from malaria_web.models import Posts
from profile.models import *

from pcsa.utils import (
    create_admin,
    create_pcsapost_with_details,
    create_malariapost_with_details,
    create_pcuser
    )

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Settings(LiveServerTestCase):
    '''
    Settings Class contains UI testcases for `Posts` tab in
    Pcuser profile. This view consists of PCsa Post, Malaria Post, Profile,
    Edit profile tabs.
    Pcsa Post:
        - Null values in Create and edit post form
        - Create post
        - Edit post
        - Delete post with No Associated pcuser
        - Delete post with Associated pcuser
    Malaria post:
        - Null values in Create and edit Malaria post form
        - Create Malaria post without any pcuser
        - Edit Malaria post
        - Create/Edit Malaria post with invalid dates
      
    Profile:
        - Display correct null values in profile page
        - Display correct details of the user
        - Edit details and check again

    Additional Note:
    It needs to be ensured that the dates in the test functions
    given below are later than the current date so that there are no
    failures while creating an event. Due to this reason, the date
    at several places has been updated to 2017
    '''

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.settings = EventsPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        cls.elements = EventsPageLocators()
        super(Settings, cls).setUpClass()

    def setUp(self):
        create_admin()
        self.login_admin()
        self.settings.go_to_events_page()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(Settings, cls).tearDownClass()

    def login_admin(self):
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({'username' : 'admin', 'password' : 'admin'})

    def delete_profile_from_list(self):
        settings = self.settings
        self.assertEqual(settings.element_by_xpath(
            self.elements.DELETE_PCUSER).text, 'Delete')
        settings.element_by_xpath(
            self.elements.DELETE_PCUSER+'//a').click()
        self.assertNotEqual(settings.get_deletion_box(), None)
        self.assertEqual(settings.get_deletion_context(), 'Delete Profile')
        settings.submit_form()

    def delete_profile_data_from_list(self):
        settings = self.settings
        self.assertEqual(settings.element_by_xpath(
            self.elements.DELETE_PCUSER_DETAILS).text, 'Delete')
        settings.element_by_xpath(
            self.elements.DELETE_PCUSER_DETAILS+'//a').click()

        self.assertNotEqual(settings.get_deletion_box(), None)
        self.assertEqual(settings.get_deletion_context(), 'Delete Profile Data')
        settings.submit_form()


    def delete_pcuser_post_from_list(self):
        settings = self.settings
        self.assertEqual(settings.element_by_xpath(
            self.elements.DELETE_PCUSER_POST).text, 'Delete')
        settings.element_by_xpath(
            self.elements.DELETE_PCUSER_POST+'//a').click()

        # confirm on delete
        self.assertNotEqual(settings.get_deletion_box(), None)
        self.assertEqual(settings.get_deletion_context(), 'Delete Posts by Pcuser')
        settings.submit_form()

    def test_profile_tab(self):
        settings = self.settings
        self.assertEqual(settings.get_message_context(),
            'There are currently no posts by you.')

    def test_pcsa_post_tab_and_create_pcsa_post_without_pcuser(self):
        settings = self.settings
        settings.click_link(settings.jobs_tab)
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + settings.job_list_page)
        self.assertEqual(settings.get_message_context(),
            'There are currently no pcusers associated. Please add a Pcuser to create a new post')

        settings.click_link('Edit Pcsa Post')
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + settings.edit_pcsa_post_page)
        self.assertEqual(settings.get_message_context(),
            'Please create a Pcsa Post first.')

    def test_create_pcsa_post(self):
        settings = self.settings
        event = ['post-name', '2017-08-21', '2017-09-28']
        settings.go_to_create_pcsa_post_page()
        settings.fill_create_pcsa_post_form(pcsa_post)

        # check pcsa post created
        self.assertEqual(self.driver.current_url,
            self.live_server_url + settings.pcsa_post_list_page)
        self.assertEqual(settings.get_pcsa_post_name(), 'post-name')

        # database check to see if correct post created
        self.assertEqual(len(PcsaPost.objects.all()), 1)
        self.assertNotEqual(len(PcsaPost.objects.filter(name=pcsa_post[0])), 0)

    # - commented out due to bug - desirable feature not yet implemented
    """def test_duplicate_event(self):
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)
        settings = self.settings
        # check event created
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + settings.event_list_page)
        self.assertEqual(settings.get_event_name(), 'event-name')
        settings.go_to_create_event_page()
        settings.fill_event_form(event)
        # database check to verify that event is not created
        self.assertEqual(len(Event.objects.all()), 1)
        # TBA here - more checks depending on behaviour that should be reflected
        self.assertNotEqual(self.driver.current_url,
                            self.live_server_url + settings.event_list_page)"""

    def test_edit_pcsa_post(self):
        event = ['post-name', '2017-08-21', '2017-09-28']
        created_pcsa_post = create_pcsa_post_with_details(pcsa_post)

        settings = self.settings
        settings.live_server_url = self.live_server_url

        # create pcsapost
        settings.navigate_to_pcsa_post_list_view()
        self.assertEqual(settings.get_pcsa_post_name(), created_pcsa_post.name)

        settings.go_to_edit_pcsa_post_page()
        edited_pcsa_post = ['new-post-name', '2017-09-21', '2017-09-28']
        settings.fill_pcsa_post_form(edited_pcsa_post)

        # check pcsapost edited
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + settings.pcsa_post_list_page)
        self.assertEqual(settings.get_pcsa_post_name(), 'new-post-name')

        # database check to see if pcsa post edited with correct details
        self.assertEqual(len(PcsaPost.objects.all()), 1)
        self.assertNotEqual(len(PcsaPost.objects.filter(name=edited_pcsa_post[0])), 0)

    def test_create_and_edit_pcsa_post_with_invalid_details(self):
        
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.go_to_create_pcsa_post_page()
        invalid_post = ['post-name-invalid', '05/17/2016', '09/28/2016']
        settings.fill_pcsa_post_form(invalid_post)

        # check event not created and error message displayed
        self.assertNotEqual(self.driver.current_url,
            self.live_server_url + settings.pcsa_post_list_page)
        self.assertEqual(settings.get_warning_context(),
            "Start date should be today's date or later.")

        # database check to see that no pcsapost created
        self.assertEqual(len(PcsaPost.objects.all()), 0)

        settings.navigate_to_pcsa_post_list_view()
        settings.go_to_create_pcsa_post_page()
        valid_pcsa_post = ['post-name', '2017-05-21', '2017-09-28']
        valid_pcsa_post_created = create_pcsa_post_with_details(valid_pcsa_post)

        settings.navigate_to_pcsa_post_list_view()
        self.assertEqual(settings.get_pcsa_post_name(), valid_pcsa_post_created.name)

        settings.go_to_edit_pcsa_post_page()
        settings.fill_pcsa_post_form(invalid_post)

        # check pcsa post not edited and error message displayed
        self.assertNotEqual(self.driver.current_url,
            self.live_server_url +settings.pcsa_post_list_page)
        self.assertEqual(settings.get_warning_context(),
            "Start date should be today's date or later.")

        # database check to ensure that post not edited
        self.assertEqual(len(PcsaPost.objects.all()), 1)
        self.assertEqual(len(PcsaPost.objects.filter(name=invalid_pcsa_post[0])), 0)

    def test_edit_pcsa_post_with_elapsed_start_date(self):
        elapsed_post = ['post-name', '2016-05-21', '2017-08-09']

        # Create a pcsa post with elapsed start date
        created_post = create_pcsa_post_with_details(elapsed_post)

        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_pcsa_post_list_view()
        self.assertEqual(settings.get_pcsa_post_name(), created_post.name)

        settings.go_to_edit_pcsa_post_page()

        # Try editing any one field - (event name in this case)
        settings.element_by_xpath(self.elements.CREATE_PCSAPOST_NAME).clear()
        settings.send_value_to_xpath(self.elements.CREATE_PCSAPOST_NAME,
            'changed-post-name')
        settings.submit_form()

        # check post not edited
        self.assertNotEqual(self.driver.current_url,
            self.live_server_url + settings.pcsa_post_list_page)

        # Test for proper msg TBA later once it is implemented

        # database check to ensure that post not edited
        self.assertEqual(len(Event.objects.all()), 1)
        self.assertNotEqual(len(Event.objects.filter(name=elapsed_pcsa_post[0])), 0)

    def test_edit_pcsa_post_with_invalid_start_date(self):
        pcsa_post = ['post-name', '2017-08-21', '2017-09-28']
        created_pcsa_post = create_pcsa_post_with_details(pcsa_post)

        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_pcsa_post_list_view()

        self.assertEqual(settings.get_pcsa_post_name(), created_pcsa_post.name)
        settings.go_to_edit_pcsa_post_page()

        # Edit pcsa post such that it is no longer in the new date range
        new_pcsa_post = ['new-post-name', '2017-08-30', '2017-09-21']
        settings.fill_pcsa_post_form(new_pcsa_post)

        # check post not edited and error message displayed
        self.assertNotEqual(self.driver.current_url,
            self.live_server_url + settings.event_list_page)
        self.assertEqual(
            settings.element_by_xpath(self.elements.TEMPLATE_ERROR_MESSAGE).text,
            'You cannot edit this post as the following associated job no longer lies within the new date range :')

        # database check to ensure that event not edited
        self.assertEqual(len(PcsaPost.objects.all()), 1)
        self.assertEqual(len(PcsaPost.objects.filter(name=new_pcsa_post[0])), 0)

    def test_delete_pcsa_post_with_no_associated_pcuser(self):
        pcsa_post = ['post-name', '2017-08-21', '2017-09-28']
        created_pcsa_post = create_pcsa_post_with_details(pcsa_post)

        # create post
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_pcsa_post_list_view()
        self.assertEqual(settings.get_pcsa_post_name(), created_pcsa_post.name)

        self.delete_pcsa_post_from_list()

        # check post deleted
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + settings.pcsa_post_list_page)
        with self.assertRaises(NoSuchElementException):
            settings.get_results()

        # database check to ensure that post is deleted
        self.assertEqual(len(PcsaPost.objects.all()), 0)

    def test_delete_pcsa_post_with_associated_date(self):
        pcsa_post = ['post-name', '2017-08-21', '2017-09-28']
        created_pcsa_post = create_pcsa_post_with_details(pcsa_post)

        settings = self.settings
        settings.live_server_url = self.live_server_url

        # check post created
        settings.navigate_to_pcsa_post_list_view()
        self.assertEqual(settings.get_pcsa_post_name(), created_pcsa_post.name)

        # delete post
        self.delete_pcsa_post_from_list()

        self.assertNotEqual(settings.get_danger_message(), None)
        self.assertEqual(settings.get_template_error_message(),
            'You cannot delete a post that a different user is currently associated with.')

        # check post NOT deleted
        settings.navigate_to_pcsa_post_list_view()
        self.assertEqual(settings.get_pcsa_post_name(), 'post-name')

        # database check to ensure that post is not deleted
        self.assertEqual(len(PcsaPost.objects.all()), 1)
        self.assertNotEqual(len(PcsaPost.objects.filter(name = created_pcsa_post.name)), 0)

    def test_create_malaria_post(self):

        malaria_post = ['post-name', '2017-08-21', '2017-09-28']
        created_malaria_post = create_malaria_post_with_details(malaria_post)

        settings = self.settings
        settings.live_server_url = self.live_server_url

        # create post
        malaria_post = ['post-name','post name','post description',
            '2017-08-21', '2017-08-28']
        settings.go_to_create_malaria_post_page()
        settings.fill_malaria_post_form(malaria_post)

        # check post created
        settings.navigate_to_malaria_post_list_view()
        self.assertEqual(settings.get_malaria_post_name(), 'post name')
        self.assertEqual(settings.get_malaria_post_event(), created_malaria_post.name)

        # database check to ensure that correct job created
        self.assertEqual(len(MalariaPost.objects.all()), 1)
        self.assertNotEqual(len(MalariaPost.objects.filter(name=MalariaPost[1])), 0)

    # - commented out due to bug - desirable feature not yet implemented
    """def test_duplicate_job(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)
        # create job
        job = ['event-name','job name','job description',
            '2017-08-21', '2017-08-28']
        create_job_with_details(job))
        settings = self.settings
        # check job created
        settings.navigate_to_job_list_view(self.live_server_url)
        self.assertEqual(settings.get_job_name(), 'job name')
        self.assertEqual(settings.get_job_event(), 'event-name')
        # Create another job with same details within the same event
        settings.go_to_create_job_page()
        settings.fill_job_form(job)
        # database check to ensure that job not created
        self.assertEqual(len(Job.objects.all()), 1)
        # TBA here - more checks depending on logic that should be reflected
        # check job not created - commented out due to bug
        self.assertNotEqual(self.driver.current_url,
                            self.live_server_url + settings.job_list_page)"""

    def test_edit_malaria_post(self):
    
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create malaria_post
        post = ['post', '2017-08-21', '2017-08-21', '',created_post]
        created_post = create_malaria_post_with_details(malaria_post)

        settings = self.settings
        settings.live_server_url = self.live_server_url

        edit_malaria_post = ['malaria_post-name','changed malaria_post name','malaria_post description',
            '2017-08-25', '2017-08-25']
        settings.navigate_to_malaria_post_list_view()
        settings.go_to_edit_malaria_post_page()
        settings.fill_malaria_post_form(edit_malaria_post)

        # check job edited
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + settings.job_list_page)
        self.assertEqual(settings.get_job_name(), 'changed job name')

        # database check to ensure that job edited correctly
        self.assertEqual(len(Job.objects.all()), 1)
        self.assertNotEqual(len(Job.objects.filter(name=edit_job[1])), 0)


    def test_edit_malaria_post_with_invalid_date(self):

        malaria_post = ['post-name', '2017-08-21', '2017-09-28']
        created_malaria_post = create_malaria_post_with_details(malaria_post)

        malaria_post = ['job', '2017-08-21', '2017-08-21', '',created_malaria_post]
        created_malaria_post = create_malaria_post_with_details(malaria_post)

        invalid_malaria_post_one = ['malaria_post-name','changed malaria_post name','malaria_post description',
            '2017-05-03', '2017-11-09']

        settings = self.settings
        settings.live_server_url = self.live_server_url

        # edit malaria_post with start date outside start date
        settings.navigate_to_malaria_post_list_view()
        settings.go_to_edit_malaria_post_page()
        settings.fill_malaria_post_form(invalid_malaria_post_one)

        # check malaria_post not edited and proper error message displayed
        self.assertNotEqual(self.driver.current_url,
            self.live_server_url +settings.malaria_post_list_page)
        self.assertEqual(settings.get_warning_context(),
            'Post dates should lie within Post dates')

        # database check to ensure that post is not edited
        self.assertEqual(len(MalariaPost.objects.all()), 1)
        self.assertEqual(len(MalariaPost.objects.filter(name=invalid_malaria_post_one[1])), 0)

        invalid_malaria_post_two = ['malaria_post-name','changed malaria_post name','malaria_post description',
            '2017-09-14', '2017-12-31']
        settings.navigate_to_malaria_post_list_view()
        settings.go_to_edit_malaria_post_page()
        settings.fill_malaria_post_form(invalid_malaria_post_two)

        # check post not edited and proper error message displayed
        self.assertNotEqual(self.driver.current_url,
            self.live_server_url +settings.job_list_page)
        self.assertEqual(settings.get_warning_context(),
            'Post dates should lie within Event dates')

        # database check to ensure that Post not edited
        self.assertEqual(len(MalariaPost.objects.all()), 1)
        self.assertEqual(len(MalariaPost.objects.filter(name=invalid_malaria_post_two[1])), 0)

    def test_edit_malaria_post_with_invalid_date(self):
        malaria_post = ['event-name', '2017-08-21', '2017-09-28']
        created_malaria_post = create_malaria_post_with_details(malaria_post)

        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_job_list_view()

        invalid_malaria_post_one = ['malaria_post-name','changed malaria_post name','malaria_post description',
            '2017-09-01', '2017-09-11']

        # edit malaria_post with date range such that the start date no longer
        # falls in the range
        settings.go_to_edit_malaria_post_page()
        settings.fill_malaria_post_form(invalid_malaria_post_one)

        # check malaria_post not edited and proper error message displayed
        self.assertNotEqual(self.driver.current_url,
            self.live_server_url +settings.malaria_post_list_page)
        self.assertEqual(settings.get_template_error_message(),
            'You cannot edit this malaria post as 1 associated shift no longer lies within the new date range')

        self.assertEqual(len(MalariaPost.objects.all()), 1)
        self.assertNotEqual(len(MalariaPost.objects.filter(name=created_malaria_post.name)), 0)

    def test_delete_job_without_associated_pcuser(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-21', '',created_event]
        created_job = create_job_with_details(job)

        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_job_list_view()
        self.assertEqual(settings.get_job_name(), 'job')
        self.assertEqual(settings.get_job_event(), 'event-name')

        # delete job
        self.delete_job_from_list()

        # check event deleted
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + settings.job_list_page)
        with self.assertRaises(NoSuchElementException):
            settings.get_results()

        # database check to ensure that job is deleted
        self.assertEqual(len(Job.objects.all()), 0)

    def test_delete_job_with_associated_pcuser(self):

        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-21', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2017-08-21', '09:00', '12:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        settings = self.settings
        settings.live_server_url = self.live_server_url

        # delete job
        settings.navigate_to_job_list_view()
        self.delete_job_from_list()

        self.assertNotEqual(settings.get_danger_message(), None)
        self.assertEqual(settings.get_template_error_message(),
            'You cannot delete a job that a shift is currently associated with.')

        # check job NOT deleted
        settings.navigate_to_job_list_view()
        self.assertEqual(settings.get_job_name(), 'job')

        # database check to ensure that job is not deleted
        self.assertEqual(len(Job.objects.all()), 1)
        self.assertNotEqual(len(Job.objects.filter(name = created_job.name)), 0)

    def test_create_shift(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        settings = self.settings
        settings.live_server_url = self.live_server_url

        # create shift
        settings.navigate_to_shift_list_view()
        settings.go_to_create_shift_page()

        shift = ['08/30/2017', '09:00', '12:00', '10']
        settings.fill_shift_form(shift)

        # verify that shift was created
        self.assertNotEqual(settings.get_results(), None)
        with self.assertRaises(NoSuchElementException):
            settings.get_help_block()

        # database check to ensure that shift created with proper job
        self.assertEqual(len(Shift.objects.all()), 1)
        self.assertNotEqual(len(Shift.objects.filter(job=created_job)), 0)

    def test_create_shift_with_invalid_timings(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        settings = self.settings
        settings.live_server_url = self.live_server_url

        # create job
        job = ['job', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        settings.navigate_to_shift_list_view()
        settings.go_to_create_shift_page()

        # create shift where end hours is less than start hours
        shift = ['08/30/2017', '14:00', '12:00', '5']
        settings.fill_shift_form(shift)

        # verify that shift was not created and error message displayed
        self.assertEqual(settings.get_warning_context(),
            'Shift end time should be greater than start time')

        # database check to ensure that shift is not created
        self.assertEqual(len(Shift.objects.all()), 0)

    def test_edit_shift_with_invalid_timings(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2017-08-21', '09:00', '12:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_shift_list_view()
        settings.go_to_edit_shift_page()

        # edit shift with end hours less than start hours
        invalid_shift = ['08/30/2017', '18:00', '13:00', '5']
        settings.fill_shift_form(invalid_shift)

        # verify that shift was not edited and error message displayed
        self.assertEqual(settings.get_warning_context(),
            'Shift end time should be greater than start time')

        # database check to ensure that shift was not edited
        self.assertEqual(len(Shift.objects.all()), 1)
        self.assertNotEqual(len(Shift.objects.filter(date=created_shift.date)), 0)

    def test_create_shift_with_invalid_date(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        settings = self.settings
        settings.live_server_url = self.live_server_url

        # create shift
        settings.navigate_to_shift_list_view()
        settings.go_to_create_shift_page()

        shift = ['06/30/2017', '14:00', '18:00', '5']
        settings.fill_shift_form(shift)

        # verify that shift was not created and error message displayed
        self.assertEqual(settings.get_warning_context(),
            'Shift date should lie within Job dates')

        # database check to ensure that shift was not created
        self.assertEqual(len(Shift.objects.all()), 0)

    def test_edit_shift_with_invalid_date(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2017-08-21', '09:00', '12:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_shift_list_view()
        settings.go_to_edit_shift_page()

        # edit shift with date not between job dates
        invalid_shift = ['02/05/2017', '04:00', '13:00', '2']
        settings.fill_shift_form(invalid_shift)

        # verify that shift was not edited and error message displayed
        self.assertEqual(settings.get_warning_context(),
            'Shift date should lie within Job dates')

        # database check to ensure that shift was not edited
        self.assertEqual(len(Shift.objects.all()), 1)
        self.assertNotEqual(len(Shift.objects.filter(date=created_shift.date)), 0)

    def test_edit_shift(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2017-08-21', '09:00', '12:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_shift_list_view()
        settings.go_to_edit_shift_page()

        # edit shift with date between job dates
        shift = ['08/25/2017', '10:00', '13:00', '2']
        settings.fill_shift_form(shift)

        with self.assertRaises(NoSuchElementException):
            settings.get_help_block()

        self.assertEqual(settings.get_shift_date(), 'Aug. 25, 2017')

        # database check to ensure that shift was edited
        self.assertEqual(len(Shift.objects.all()), 1)
        self.assertEqual(len(Shift.objects.filter(date=created_shift.date)), 0)

    def test_delete_shift(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2017-08-21', '09:00', '12:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_shift_list_view()
        self.assertNotEqual(settings.get_results(), None)

        # delete shift
        self.delete_shift_from_list()

        # check deletion of shift
        settings.navigate_to_shift_list_view()
        self.assertEqual(settings.get_message_context(),
            'There are currently no shifts. Please create shifts first.')

        # database check to ensure that shift is deleted
        self.assertEqual(len(Shift.objects.all()), 0)

    def test_delete_shift_with_pcuser(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2017-08-21', '09:00', '12:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        # create pcuser for shift
        pcuser = create_pcuser()
        shift_pcuser = register_pcuser_for_shift_utility(
            created_shift, pcuser)

        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_shift_list_view()

        # delete shift
        self.delete_shift_from_list()

        # check error message displayed and shift not deleted
        self.assertEqual(settings.get_template_error_message(),
            'You cannot delete a shift that a pcuser has signed up for.')

        # database check to ensure that shift is not deleted
        self.assertEqual(len(Shift.objects.all()), 1)
        self.assertNotEqual(len(Shift.objects.filter(date = created_shift.date)), 0)

    def test_organization(self):

        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.click_link(settings.organization_tab)
        self.assertEqual(self.driver.current_url,
            self.live_server_url +settings.organization_list_page)

        settings.click_link('Create Organization')
        self.assertEqual(self.driver.current_url,
            self.live_server_url +settings.create_organization_page)

        # Test all valid characters for organization
        # [(A-Z)|(a-z)|(0-9)|(\s)|(\-)|(:)]
        settings.fill_organization_form('Org-name 92:4 CA')
        self.assertEqual(settings.get_org_name(), 'Org-name 92:4 CA')

        # database check to ensure that organization is created
        self.assertEqual(len(Organization.objects.all()), 1)
        self.assertNotEqual(len(Organization.objects.filter(name='Org-name 92:4 CA')), 0)

    def test_replication_of_organization(self):
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_organization_view()
        settings.go_to_create_organization_page()

        settings.fill_organization_form('Organization')
        self.assertEqual(settings.get_org_name(), 'Organization')

        # Create same orgnization again
        settings.go_to_create_organization_page()
        settings.fill_organization_form('Organization')

        self.assertEqual(settings.get_help_block().text,
            'Organization with this Name already exists.')
        
        # database check to ensure that duplicate organization is created
        self.assertEqual(len(Organization.objects.all()), 1)

    def test_edit_org(self):
        # create org
        org = create_organization()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_organization_view()

        # edit org
        self.assertEqual(settings.element_by_xpath(self.elements.EDIT_ORG).text, 'Edit')
        settings.element_by_xpath(self.elements.EDIT_ORG+'//a').click()

        settings.fill_organization_form('changed-organization')

        # check edited org
        org_list = []
        org_list.append(settings.get_org_name())

        self.assertTrue('changed-organization' in org_list)

        # database check to ensure that organization is edited
        self.assertEqual(len(Organization.objects.all()), 1)
        self.assertNotEqual(len(Organization.objects.filter(name='changed-organization')), 0)

    def test_delete_org_without_associated_users(self):
        # create org
        org = create_organization()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_organization_view()

        # delete org
        self.delete_organization_from_list()

        # check org deleted
        with self.assertRaises(NoSuchElementException):
            settings.element_by_xpath('//table//tbody//tr[1]')

        # database check to ensure that organization is deleted
        self.assertEqual(len(Organization.objects.all()), 0)

    def test_delete_org_with_associated_users(self):
        # create org
        org = create_organization()
        pcuser = create_pcuser()

        pcuser.organization = org
        pcuser.save()

        # delete org
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_organization_view()
        self.delete_organization_from_list()

        # check org not deleted message received
        self.assertNotEqual(settings.get_danger_message(), None)
        self.assertEqual(settings.get_template_error_message(),
            'You cannot delete an organization that users are currently associated with.')

        # database check to ensure that organization is not deleted
        self.assertEqual(len(Organization.objects.all()), 1)
	self.assertNotEqual(len(Organization.objects.filter(name=org.name)), 0)
