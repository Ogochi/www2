from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from datetime import timedelta


class Airplane(models.Model):
    registerNumber = models.CharField(max_length=255, unique=True)
    places = models.IntegerField()

    def clean(self):
        if self.places < 0:
            raise ValidationError('Airplane can not have less than 0 places!')

    def __str__(self):
        return 'Airplane %s' % self.registerNumber


class Passenger(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    class Meta:
        unique_together = ('name', 'surname')

    def __str__(self):
        return 'Passenger %s %s' % (self.name, self.surname)


class Flight(models.Model):
    startAirport = models.CharField(max_length=255)
    endAirport = models.CharField(max_length=255)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)

    def clean(self):
        if self.endTime < self.startTime:
            raise ValidationError('End time is before start time!')
        dateDiff = self.endTime - self.startTime
        if dateDiff < timedelta(minutes=30):
            raise ValidationError('Flight is shorter than 30 min!')

        for flight in Flight.objects.filter(airplane=self.airplane):
            if flight.startTime <= self.startTime <= flight.endTime \
                    or flight.startTime <= self.endTime <= flight.endTime:
                raise ValidationError('Airplane can not have two flights in the same time!')

        flightsInStartDay = Flight.objects.filter(airplane=self.airplane).filter(
            Q(startTime__day=self.startTime.day) | Q(endTime__day=self.startTime.day))
        if flightsInStartDay.values('pk').distinct().count() == 4:
            raise ValidationError('Can not have more than 4 flights in the same day for one airplane!')
        flightsInEndDay = Flight.objects.filter(airplane=self.airplane).filter(
            Q(startTime__day=self.endTime.day) | Q(endTime__day=self.endTime.day))
        if flightsInEndDay.values('pk').distinct().count() == 4:
            raise ValidationError('Can not have more than 4 flights in the same day for one airplane!')

    def __str__(self):
        return 'Flight from %s to %s' % (self.startAirport, self.endAirport)


class Ticket(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)

    def clean(self):
        currPassengersNum = Ticket.objects.filter(flight=self.flight).count()
        airplanePlaces = Flight.objects.get(pk=self.flight.pk).airplane.places
        if currPassengersNum == airplanePlaces:
            raise ValidationError('There are not empty places in airplane!')
