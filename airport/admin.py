from django.contrib import admin
from .models import Airplane, Passenger, Flight, FlightPassenger

admin.site.register(Airplane)
admin.site.register(Passenger)
admin.site.register(Flight)
admin.site.register(FlightPassenger)
