from event.models import Event
from job.models import Job
from administrator.models import Administrator
from django.contrib.auth.models import User
from shift.models import Shift, VolunteerShift
from volunteer.models import Volunteer
from organization.models import Organization
from cities_light.models import Country

# Contains common functions which need to be frequently called by tests

def clear_objects():
    """
    - Deletes objects from multiple tables
    - Called once all tests in a module are completed
    """
    
    VolunteerShift.objects.all().delete()
    Volunteer.objects.all().delete()
    User.objects.all().delete()
    Shift.objects.all().delete()
    Job.objects.all().delete()
    Event.objects.all().delete()
    Organization.objects.all().delete()

def create_event_with_details(event):
    """
    Creates and returns event with passed name and dates
    """
    e1 = Event(
        name=event[0],
        start_date=event[1],
        end_date=event[2]
        )
    e1.save()
    return e1

def create_job_with_details(job):
    """
    Creates and returns job with passed name and dates
    """
    
    j1 = Job(
        name=job[0],
        start_date=job[1],
        end_date=job[2],
        description=job[3],
        event=job[4]
        )

    j1.save()
    return j1

def create_volunteer_with_details(volunteer):
    """
    Creates and returns volunteer with passed name and dates
    """
    u1 = User.objects.create_user(volunteer[0])
    v1 = Volunteer(
        first_name=volunteer[1],
        last_name=volunteer[2],
        address=volunteer[3],
        city=volunteer[4],
        state=volunteer[5],
        country=volunteer[6],
        phone_number=volunteer[7],
        email=volunteer[8],
        user=u1
        )
    v1.save()
    return v1

def create_shift_with_details(shift):
    """
    Creates and returns shift with passed name and dates
    """
    s1 = Shift(
        date=shift[0],
        start_time=shift[1],
        end_time=shift[2],
        max_volunteers=shift[3],
        job=shift[4]
        )
    s1.save()
    return s1

def set_shift_location(shift,loc):
    """
    Sets and returns shift with passed location details
    """
    shift.address=loc[0]
    shift.city=loc[1]
    shift.state=loc[2]
    shift.country=loc[3]
    shift.venue=loc[4]
    
    shift.save()
    return shift

def get_report_list(duration_list, report_list, total_hours):
    """
    - Contains steps to generate report list with passes parameters
    - Called frequently by test case in shift unit tests
    """

    for duration in duration_list:
		total_hours += duration
		report = {}
		report["duration"] = duration
		report_list.append(report)

    return (report_list, total_hours)

def create_organization():
    Organization.objects.create(
        name = 'DummyOrg')

def create_country():
    Country.objects.create(
        name_ascii = 'India',
        slug ='india',
        geoname_id = '1269750',
        alternate_names = '',
        name = 'India',
        code2 = 'IN',
        code3 = 'IND',
        continent = 'AS',
        tld = 'in',
        phone = '91')

def create_admin():

    user_1 = User.objects.create_user(
        username = 'admin',
        password = 'admin'
        )

    admin = Administrator.objects.create(
        user = user_1,
        address = 'address',
        city = 'city',
        state = 'state',
        country = 'country',
        phone_number = '9999999999',
        email = 'admin@admin.com',
        unlisted_organization = 'organization')

    return admin

def create_volunteer():

    user_1 = User.objects.create_user(
        username = 'volunteer',
        password = 'volunteer'
        )

    volunteer = Volunteer.objects.create(
        user = user_1,
        address = 'address',
        city = 'city',
        state = 'state',
        country = 'country',
        phone_number = '9999999999',
        email = 'volunteer@volunteer.com',
        unlisted_organization = 'organization')

    return volunteer

