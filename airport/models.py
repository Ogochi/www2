from django.db import models


class Airplane(models.Model):
    registerNumber = models.CharField(max_length=255, unique=True)
    places = models.IntegerField()

    def __str__(self):
        return 'Airplane %s' % self.registerNumber


class Passenger(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    def __str__(self):
        return 'Passenger %s %s' % (self.name, self.surname)


class Flight(models.Model):
    startAirport = models.CharField(max_length=255)
    endAirport = models.CharField(max_length=255)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()

    def __str__(self):
        return 'Flight from %s to %s' % (self.startAirport, self.endAirport)


class FlightPassenger(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
