# Second script for inserting to database random data


from airport.models import AirplaneCrew
from random import randint
from datetime import datetime as dt, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError

names = ['Alphonse', 'Brad', 'John', 'Ben', 'Josh', 'Alex', 'Chad']
surnames = ['Elric', 'Potter', 'Moon', 'Destroyer', 'Drake']

for i in names:
    for j in surnames:
        AirplaneCrew.objects.create(captainsName=i, captainsSurname=j)
