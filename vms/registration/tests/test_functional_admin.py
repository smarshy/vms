from django.contrib.staticfiles.testing import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import re

from organization.models import Organization
from shift.utils import create_organization, create_country

class SignUpAdmin(LiveServerTestCase):
    '''
    SignUpAdmin Class contains tests to register a admin User
    Tests included.

    Name Fields:
        - Test Null values
        - Test legit characters in first_name, last_name fields
        - Register admin with already registered username
        - Test length of name fields ( 30 char, limit)

    Location Field (Address, City, State, Country):
        - Test Null Values
        - Test legit characters as per Models defined

    Email Field:
        - Test Null Values
        - Test uniqueness of field

    Phone Number Field:
        - Test Null Values
        - Test validity of number against country entered
        - Test legit characters as per Models defined

    Organization Field:
        - Test Null Values
        - Test legit characters as per Models defined

    Retention of fields:
        - Field values are checked to see that they are not lost when the page gets reloaded
    '''

    @classmethod
    def setUpClass(cls):
        cls.homepage = '/'
        cls.admin_registration_page = '/registration/signup_administrator/'
        cls.authentication_page = '/authentication/login/'
        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        super(SignUpAdmin, cls).setUpClass()

    def setUp(self):
        # create an org prior to registration. Bug in Code
        # added to pass CI
        create_organization()

        # country created so that phone number can be checked
        create_country()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(SignUpAdmin, cls).tearDownClass()

    def fill_registration_form(self, info):
        self.driver.find_element_by_id('id_username').send_keys(info[0])
        self.driver.find_element_by_id('id_password').send_keys(info[1])
        self.driver.find_element_by_id('id_first_name').send_keys(info[2])
        self.driver.find_element_by_id('id_last_name').send_keys(info[3])
        self.driver.find_element_by_id('id_email').send_keys(info[4])
        self.driver.find_element_by_id('id_address').send_keys(info[5])
        self.driver.find_element_by_id('id_city').send_keys(info[6])
        self.driver.find_element_by_id('id_state').send_keys(info[7])
        self.driver.find_element_by_id('id_country').send_keys(info[8])
        self.driver.find_element_by_id('id_phone_number').send_keys(info[9])
        self.driver.find_element_by_id('id_unlisted_organization').send_keys(info[10])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def verify_field_values(self, info):
        self.assertEqual(self.driver.find_element_by_id('id_username').get_attribute('value'),info[0])
        self.assertEqual(self.driver.find_element_by_id('id_first_name').get_attribute('value'),info[1])
        self.assertEqual(self.driver.find_element_by_id('id_last_name').get_attribute('value'),info[2])
        self.assertEqual(self.driver.find_element_by_id('id_email').get_attribute('value'),info[3])
        self.assertEqual(self.driver.find_element_by_id('id_address').get_attribute('value'),info[4])
        self.assertEqual(self.driver.find_element_by_id('id_city').get_attribute('value'),info[5])
        self.assertEqual(self.driver.find_element_by_id('id_state').get_attribute('value'),info[6])
        self.assertEqual(self.driver.find_element_by_id('id_country').get_attribute('value'),info[7])
        self.assertEqual(self.driver.find_element_by_id('id_phone_number').get_attribute('value'),info[8])
        self.assertEqual(self.driver.find_element_by_id('id_unlisted_organization').get_attribute('value'),info[9])

    def register_valid_details(self):
        self.driver.get(self.live_server_url + self.admin_registration_page)
        entry = ['admin-username','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','admin-email@systers.org','admin-address','admin-city','admin-state','admin-country','9999999999','admin-org']
        self.fill_registration_form(entry)

    def test_null_values(self):
        self.driver.get(self.live_server_url + self.admin_registration_page)

        entry = ['','','','','','','','','','','']
        self.fill_registration_form(entry)

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        # verify that 10 of the fields are compulsory
        self.assertEqual(len(self.driver.find_elements_by_class_name('help-block')),
                10)

    def test_successful_registration(self):
        self.register_valid_details()
        self.assertNotEqual(self.driver.find_elements_by_class_name('messages'),
                None)
        self.assertEqual(self.driver.find_element_by_class_name('messages').text,
                'You have successfully registered!')

    def test_name_fields(self):
        # register valid admin user
        self.register_valid_details()

        self.assertNotEqual(self.driver.find_elements_by_class_name('messages'),
                None)
        self.assertEqual(self.driver.find_element_by_class_name('messages').text,
                'You have successfully registered!')

        # register a user again with username same as already registered user
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        self.driver.get(self.live_server_url + self.admin_registration_page)

        entry = ['admin-username','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','admin-email1@systers.org','admin-address','admin-city','admin-state','admin-country','9999999999','admin-org']
        self.fill_registration_form(entry)

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_username')/div/p/strong").text,
                'User with this Username already exists.')

        # test numeric characters in first-name, last-name
        self.driver.get(self.live_server_url + self.admin_registration_page)

        entry = ['admin-username-1','admin-password!@#$%^&*()_','admin-first-name-1','admin-last-name-1','admin-email1@systers.org','admin-address','admin-city','admin-state','admin-country','9999999999','admin-org']
        self.fill_registration_form(entry)

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_first_name')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_last_name')/div/p/strong").text,
                'Enter a valid value.')

        # test special characters in first-name, last-name
        self.driver.get(self.live_server_url + self.admin_registration_page)

        entry = ['admin-username','admin-password!@#$%^&*()_','name-!@#$%^&*()_','name-!@#$%^&*()_','admin-email1@systers.org','admin-address','admin-city','admin-state','admin-country','9999999999','admin-org']
        self.fill_registration_form(entry)

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_first_name')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_last_name')/div/p/strong").text,
                'Enter a valid value.')

        # test length of first-name, last-name not exceed 30
        self.driver.get(self.live_server_url + self.admin_registration_page)

        entry = ['admin-username','admin-password!@#$%^&*()_','admin-first-name-!@#$%^&*()_','admin-last-name-!@#$%^&*()_','admin-email1@systers.org','admin-address','admin-city','admin-state','admin-country','9999999999','admin-org']
        self.fill_registration_form(entry)

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        error_message = self.driver.find_element_by_xpath("id('div_id_first_name')/div/p/strong").text
        self.assertTrue(bool(re.search(r'Ensure this value has at most 20 characters', str(error_message))))

        error_message = self.driver.find_element_by_xpath("id('div_id_last_name')/div/p/strong").text,
        self.assertTrue(bool(re.search(r'Ensure this value has at most 20 characters', str(error_message))))

    def test_location_fields(self):
        # test numeric characters in address, city, state, country
        self.driver.get(self.live_server_url + self.admin_registration_page)

        entry = ['admin-username-1','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','email1@systers.org','123 New-City address','1 admin-city','007 admin-state','54 admin-country','9999999999','admin-org']
        self.fill_registration_form(entry)

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.admin_registration_page)

        #verify that messages are displayed for city, state and country but not address
        self.assertEqual(len(self.driver.find_elements_by_class_name('help-block')),
                3)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_city')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_state')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_country')/div/p/strong").text,
                'Enter a valid value.')

        # test special characters in address, city, state, country
        self.driver.get(self.live_server_url + self.admin_registration_page)

        entry = ['admin-username-2','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','email2@systers.org','admin-address!@#$()','!$@%^#&admin-city','!$@%^#&admin-state','&%^*admin-country!@$#','9999999999','admin-org']
        self.fill_registration_form(entry)

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.admin_registration_page)

        # verify that messages are displayed for all fields
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_address')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_city')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_state')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_country')/div/p/strong").text,
                'Enter a valid value.')

    def test_email_field(self):

        # register valid admin user
        self.register_valid_details()

        # verify successful registration
        self.assertNotEqual(self.driver.find_elements_by_class_name('messages'),
                None)
        self.assertEqual(self.driver.find_element_by_class_name('messages').text,
                'You have successfully registered!')
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        # Try to register admin again with same email address
        self.driver.get(self.live_server_url + self.admin_registration_page)

        entry = ['admin-username-1','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','admin-email@systers.org','admin-address','admin-city','admin-state','admin-country','9999999999','admin-org']
        self.fill_registration_form(entry)

        # verify that user wasn't registered
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.admin_registration_page)
        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_email')/div/p/strong").text,
                'Administrator with this Email already exists.')

    def test_phone_field(self):

        # register valid admin user with valid phone number for country
        self.driver.get(self.live_server_url + self.admin_registration_page)

        entry = ['admin-username','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','admin-email@systers.org','admin-address','admin-city','admin-state','India','022 2403 6606','admin-org']
        self.fill_registration_form(entry)

        # verify successful registration
        self.assertNotEqual(self.driver.find_elements_by_class_name('messages'),
                None)
        self.assertEqual(self.driver.find_element_by_class_name('messages').text,
                'You have successfully registered!')
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        # Try to register admin with incorrect phone number for country
        self.driver.get(self.live_server_url + self.admin_registration_page)

        entry = ['admin-username-1','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','admin-email1@systers.org','admin-address','admin-city','admin-state','India','237937913','admin-org']
        self.fill_registration_form(entry)

        # verify that user wasn't registered
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.admin_registration_page)
        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_phone_number')/div/p/strong").text,
                "This phone number isn't valid for the selected country")

        # Use invalid characters in phone number
        self.driver.get(self.live_server_url + self.admin_registration_page)

        entry = ['admin-username-1','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','admin-email1@systers.org','admin-address','admin-city','admin-state','India','23&79^37913','admin-org']
        self.fill_registration_form(entry)

        # verify that user wasn't registered
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.admin_registration_page)
        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_phone_number')/div/p/strong").text,
                "Please enter a valid phone number")

    def test_organization_field(self):

        # test numeric characters in organization
        self.driver.get(self.live_server_url + self.admin_registration_page)

        entry = ['admin-username-1','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','email1@systers.org','admin-address','admin-city','admin-state','admin-country','9999999999','13 admin-org']
        self.fill_registration_form(entry)

        # verify successful registration
        self.assertNotEqual(self.driver.find_elements_by_class_name('messages'),
                None)
        self.assertEqual(self.driver.find_element_by_class_name('messages').text,
                'You have successfully registered!')
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        # Use invalid characters in organization
        self.driver.get(self.live_server_url + self.admin_registration_page)

        entry = ['admin-username-2','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','email2@systers.org','admin-address','admin-city','admin-state','admin-country','9999999999','!$&admin-org']
        self.fill_registration_form(entry)

        # verify that user wasn't registered
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.admin_registration_page)
        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_unlisted_organization')/div/p/strong").text,
                "Enter a valid value.")

    def test_field_value_retention(self):

        # send invalid value in fields - first name, state, phone, organization
        self.driver.get(self.live_server_url + self.admin_registration_page)

        entry = ['admin-username','admin-password!@#$%^&*()_','admin-first-name-3','admin-last-name','email1@systers.org','admin-address','admin-city','admin-state','admin-country','99999.!9999','@#admin-org']
        self.fill_registration_form(entry)

        # verify that user wasn't registered and that field values are not erased
        details = ['admin-username','admin-first-name-3','admin-last-name','email1@systers.org','admin-address','admin-city','admin-state','admin-country','99999.!9999','@#admin-org']
        self.verify_field_values(details)

        # send invalid value in fields - last name, address, city, country
        self.driver.get(self.live_server_url + self.admin_registration_page)

        entry = ['admin-username','admin-password!@#$%^&*()_','admin-first-name','admin-last-name-3','email1@systers.org','admin-address$@!','admin-city#$','admin-state','admin-country 15','99999.!9999','@#admin-org']
        self.fill_registration_form(entry)

        # verify that user wasn't registered and that field values are not erased
        details = ['admin-username','admin-first-name','admin-last-name-3','email1@systers.org','admin-address$@!','admin-city#$','admin-state','admin-country 15','99999.!9999','@#admin-org']
        self.verify_field_values(details)
