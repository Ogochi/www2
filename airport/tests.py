from django.test import TestCase
from .models import Flight, AirplaneCrew, Airplane
from django.contrib.auth.models import User
from datetime import datetime as dt, timedelta
from django.utils import timezone


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
