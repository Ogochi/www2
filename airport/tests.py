from django.test import TestCase
from .models import Flight, AirplaneCrew, Airplane
from django.contrib.auth.models import User
from datetime import datetime as dt, timedelta
from django.utils import timezone
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


# requires: export PATH=$PATH:~/www2/app
class SeleniumTest(StaticLiveServerTestCase):
    date = dt.strptime('2018-12-22', '%Y-%m-%d').astimezone(timezone.utc)

    def test(self):
        # Setup
        driver = WebDriver()
        db = {'plane': [], 'crew': [], 'flight': []}
        for i in range(5):
            a = Airplane(registerNumber=i + 10000, places=20)
            a.save()
            db['plane'].append(a)
            b = AirplaneCrew(captainsName="X{}".format(i + 10000), captainsSurname="Z{}".format(i + 1))
            b.save()
            db['crew'].append(b)
            db['flight'].append(Flight.objects.create(startAirport="A", endAirport="B", airplane=a, crew=b,
                                                      startTime=self.date, endTime=self.date + timedelta(hours=4)))
        User.objects.create_user(username='d', password='d')

        # Log in
        driver.get("{}/".format(self.live_server_url))
        driver.find_element_by_id("login_dropdown").click()
        driver.find_element_by_id("login_username").send_keys("d")
        driver.find_element_by_id("login_password").send_keys("d")
        driver.find_element_by_id("login_button").click()
        # Buying ticket
        driver.get("{}/flight/1".format(self.live_server_url))
        driver.find_element_by_id("name").send_keys("A")
        driver.find_element_by_id("surname").send_keys("B")
        driver.find_element_by_id("buy_ticket_button").click()
        # Check if bought correctly
        counter = 0
        expected_results = ["A", "B", "1"]
        for td in driver.find_elements_by_tag_name("td"):
            self.assertEqual(td.text, expected_results[counter])
            counter += 1

        # Assigning incorrect crews
        driver.get("{}/static/crews.html".format(self.live_server_url))
        driver.find_element_by_id("change_crew_assignment").click()
        Select(driver.find_element_by_id("flight_select")).select_by_index(1)
        driver.find_element_by_id("change_crew_assignment").click()
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "error_alert"))
            )
        finally:
            error_message = "Error - couldn't assign crew! You have to be logged in!"
            self.assertEqual(driver.find_element_by_class_name("alert").text, error_message)

            driver.close()


class RestApiTest(TestCase):
    date = dt.strptime('2018-12-22', '%Y-%m-%d').astimezone(timezone.utc)

    def setUp(self):
        User.objects.create_user(username='a', password='a')
        for i in range(5):
            a = Airplane.objects.create(registerNumber=i + 1, places=20)
            b = AirplaneCrew.objects.create(captainsName="X{}".format(i + 1), captainsSurname="Z{}".format(i + 1))
            Flight.objects.create(startAirport="A", endAirport="B", airplane=a, crew=b,
                                  startTime=self.date, endTime=self.date + timedelta(hours=4))

    def testGetCrews(self):
        response = self.client.get('/api/get_crews/', data={
            'day': self.date.day,
            'month': self.date.month,
            'year': self.date.year,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"crews": [{"flightId": 1, "crew": "X1 Z1"}, ' +
                         b'{"flightId": 2, "crew": "X2 Z2"}, ' + b'{"flightId": 3, "crew": "X3 Z3"}, ' +
                         b'{"flightId": 4, "crew": "X4 Z4"}, ' + b'{"flightId": 5, "crew": "X5 Z5"}]}')

    def testChangeCrewCorrect(self):
        crew = AirplaneCrew.objects.create(captainsName="Q", captainsSurname="W")
        response = self.client.post('/api/change_flight_crew/', data={
            'flightId': Flight.objects.get(airplane__registerNumber=1).id,
            'captainsName': 'Q',
            'captainsSurname': 'W',
            'username': 'a',
            'password': 'a',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Flight.objects.get(airplane__registerNumber=1).crew_id, crew.id)

    def testChangeCrewError(self):
        response = self.client.post('/api/change_flight_crew/', data={
            'flightId': Flight.objects.get(airplane__registerNumber=1).id,
            'captainsName': 'X2',
            'captainsSurname': 'Z2',
            'username': 'a',
            'password': 'a',
        })
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(Flight.objects.get(airplane__registerNumber=1).crew_id,
                            AirplaneCrew.objects.get(captainsName='X2').id)

