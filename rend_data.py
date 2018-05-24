# Script for inserting to database random data


from airport.models import Airplane, Flight
from random import randint
from datetime import datetime as dt, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError

cities = ['Warsaw', 'Copenhagen', 'Berlin', 'London', 'Paris', 'Barcelona', 'Madrid', 'Dublin', 'Oslo', 'Milan']

for i in range(50):
    print("Airplane: {}".format(i))
    num = 3*i + 1
    a = Airplane(registerNumber=num, places=randint(20, 50))
    a.full_clean()
    a.save()
    for j in range(50):
        print("\tFlight: {}".format(j))
        succeded = False
        while not succeded:
            start = randint(0, 9)
            end = randint(0, 9)
            while start == end:
                end = randint(0, 9)
            startTime = dt.now(tz=timezone.utc) + timedelta(days=randint(5, 500), hours=randint(0, 24))
            endTime = startTime + timedelta(minutes=randint(30, 300))
            f = Flight(airplane=a, startAirport=cities[start], endAirport=cities[end],
                       startTime=startTime, endTime=endTime)
            try:
                f.full_clean()
                succeded = True
            except ValidationError:
                print("Validation error!")

            f.save()
