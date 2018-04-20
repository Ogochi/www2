from airport.models import Airplane, Flight
from random import randint
from datetime import datetime as dt, timedelta
from django.utils import timezone

cities = ['Warsaw', 'Copenhagen', 'Berlin', 'London', 'Paris', 'Barcelona', 'Madrid', 'Dublin', 'Oslo', 'Milan']

for i in range(50):
    num = i + i + i + 1
    a = Airplane.objects.create(registerNumber=num, places=randint(20, 50))
    for j in range(50):
        start = randint(0, 9)
        end = randint(0, 9)
        while start == end:
            end = randint(0, 9)
        startTime = dt.now(tz=timezone.utc) + timedelta(days=randint(5, 200), hours=randint(0, 24))
        endTime = startTime + timedelta(minutes=randint(30, 300))
        Flight.objects.create(airplane=a, startAirport=cities[start], endAirport=cities[end],
                              startTime=startTime, endTime=endTime)