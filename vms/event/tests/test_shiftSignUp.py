from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User
from volunteer.models import Volunteer
from event.models import Event
from job.models import Job
from shift.models import Shift, VolunteerShift

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from shift.utils import (
    create_organization,
    create_volunteer,
    register_event_utility,
    register_job_utility,
    register_shift_utility,
    create_volunteer_with_details,
    create_shift_with_details
    )

class ShiftSignUp(LiveServerTestCase):
    '''
    '''
    @classmethod
    def setUpClass(cls):
        cls.homepage = '/'
        cls.authentication_page = '/authentication/login/'
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        super(ShiftSignUp, cls).setUpClass()

    def setUp(self):
        create_volunteer()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(ShiftSignUp, cls).tearDownClass()

    def login(self, credentials):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id('id_login').send_keys(credentials['username'])
        self.driver.find_element_by_id('id_password').send_keys(credentials['password'])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def fill_search_form(self, date):
        self.driver.find_element_by_id('from').clear()
        self.driver.find_element_by_id('to').clear()
        self.driver.find_element_by_id('from').send_keys(date[0])
        self.driver.find_element_by_id('to').send_keys(date[1])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def test_events_page_with_no_events(self):
        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})

        # open Shift Sign Up
        self.driver.find_element_by_link_text('Shift Sign Up').click()

        self.assertEqual(self.driver.find_element_by_class_name('alert-info').text,
               'There are no events.')

    def test_signup_shifts_with_registered_shifts(self):
        # login
        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})

        register_event_utility()
        register_job_utility()
        register_shift_utility()

        # open Shift Sign Up
        self.driver.find_element_by_link_text('Shift Sign Up').click()

        # on event page
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text, 'View Jobs')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # on jobs page
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text, 'View Shifts')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # on shifts page
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text, 'Sign Up')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # confirm shift assignment
        self.driver.find_element_by_xpath('//form[1]').submit()
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-danger')

        # check shift signed up
        self.assertEqual(self.driver.find_element_by_xpath(
            'html/body/div[2]/h3').text,
            'Upcoming Shifts')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text,
            'job')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[2]').text,
            'June 15, 2017')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[3]').text,
            '9 a.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text,
            '3 p.m.')

    def test_signup_for_same_shift_again(self):
        # login
        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})

        register_event_utility()
        register_job_utility()
        register_shift_utility()

        # open Shift Sign Up
        self.driver.find_element_by_link_text('Shift Sign Up').click()

        # events shown in table
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-info')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text,
            'View Jobs')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # on jobs page
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text,
            'View Shifts')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # on shifts page, Sign up this shift !
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text,
            'Sign Up')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # confirm on shift sign up
        self.driver.find_element_by_xpath('//form[1]').submit()
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-danger')

        # sign up same shift again
        # open Shift Sign Up
        self.driver.find_element_by_link_text('Shift Sign Up').click()

        # events page
        self.assertEqual(self.driver.find_element_by_class_name('alert-info').text,
               'There are no events.')
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_tag_name('table')
            self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text, 'View Jobs')

    def test_empty_events(self):
        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})

        register_event_utility()

        # open Shift Sign Up
        self.driver.find_element_by_link_text('Shift Sign Up').click()

        # on event page
        self.assertEqual(self.driver.find_element_by_class_name('alert-info').text,
               'There are no events.')
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_tag_name('table')
            self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text, 'View Jobs')

        register_job_utility()

        self.assertEqual(self.driver.find_element_by_class_name('alert-info').text,
               'There are no events.')
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_tag_name('table')
            self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text, 'View Jobs')

    def test_shift_sign_up_with_outdated_shifts(self):
        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})

        register_event_utility()
        register_job_utility()

        # create outdated shift
        shift_1 = ["2016-05-11","9:00","15:00",6,Job.objects.get(name = 'job')]
        s1 = create_shift_with_details(shift_1)

        # open Shift Sign Up
        self.driver.find_element_by_link_text('Shift Sign Up').click()

        # on event page
        self.assertEqual(self.driver.find_element_by_xpath('//table//tbody//tr[1]//td[4]').text, 'View Jobs')
        self.driver.find_element_by_xpath('//table//tbody//tr[1]//td[4]//a').click()

        # on jobs page
        self.assertEqual(self.driver.find_element_by_xpath('//table//tbody//tr[1]//td[4]').text, 'View Shifts')
        self.driver.find_element_by_xpath('//table//tbody//tr[1]//td[4]//a').click()

        self.assertEqual(self.driver.find_element_by_class_name('alert-info').text,'There are currently no shifts for the job job.')

    def test_shift_sign_up_with_no_slots(self):

        register_event_utility()
        register_job_utility()

        # create shift with no slot
        shift_2 = ["2016-05-11","9:00","15:00",1,Job.objects.get(name = 'job')]
        s2 = create_shift_with_details(shift_2)

        # Create another volunteer
        volunteer_2 = ['volunteer-2',"Sam","Turtle","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","volunteer2@volunteer.com"]
        v2 = create_volunteer_with_details(volunteer_2)

        # Assign shift to the volunteer
        VolunteerShift.objects.create(
                shift = s2,
                volunteer = v2)

        # Login as volunteer 1 and open Shift Sign Up
        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})
        self.driver.find_element_by_link_text('Shift Sign Up').click()

        # on event page
        self.assertEqual(self.driver.find_element_by_class_name('alert-info').text,'There are no events.')

    def test_search_event(self):

        register_event_utility()
        register_job_utility()
        register_shift_utility()

        # Login as volunteer 1 and open Shift Sign Up
        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})
        self.driver.find_element_by_link_text('Shift Sign Up').click()

        # enter date range in which an event starts
        date = ['05/08/2016', '08/31/2017']
        self.fill_search_form(date)
        # verify that the event shows up
        self.assertEqual(self.driver.find_element_by_xpath('//table//tbody//tr[1]//td[1]').text, 'event')

        # enter date range in which no event starts
        date = ['10/08/2016', '08/31/2017']
        self.fill_search_form(date)
        # verify that no event shows up on event page
        self.assertEqual(self.driver.find_element_by_class_name('alert-info').text,'There are no events.')

        """# enter only incorrect starting date
        date = ['10/08/2016', '']
        self.fill_search_form(date)
        # verify that no event shows up on event page
        self.assertEqual(self.driver.find_element_by_class_name('alert-info').text,'There are no events.')

        # enter only correct starting date
        date = ['05/10/2016', '']
        self.fill_search_form(date)
        # verify that the event shows up
        self.assertEqual(self.driver.find_element_by_xpath('//table//tbody//tr[1]//td[1]').text, 'event')

        # enter only incorrect ending date
        date = ['', '10/08/2015']
        self.fill_search_form(date)
        # verify that no event shows up on event page
        self.assertEqual(self.driver.find_element_by_class_name('alert-info').text,'There are no events.')

        # enter correct ending date
        date = ['', '06/15/2017']
        self.fill_search_form(date)
        # verify that the event shows up
        self.assertEqual(self.driver.find_element_by_xpath('//table//tbody//tr[1]//td[1]').text, 'event')"""
