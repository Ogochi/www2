from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as login_to_session
from django.contrib.auth.views import logout as djangoLogout
from django.contrib.auth.models import User
from .models import Flight, Passenger, Ticket
from datetime import datetime
from django.db.models import Q


def flights_list(request):
    if request.method == 'POST':
        search = datetime.strptime(request.POST['search'], '%Y-%m-%d')
        flights = Flight.objects.filter(Q(startTime__day=search.day, startTime__month=search.month) |
                                        Q(endTime__day=search.day, endTime__month=search.month)).order_by('startTime')
    else:
        flights = Flight.objects.all().order_by('startTime')
    return render(request, 'main.html', locals())


def flight(request, flightId):
    passengers = Passenger.objects.filter(
        pk__in=Ticket.objects.filter(flight=flightId).values_list('passenger', flat="True"))

    class Detail:
        def __init__(self, name, value):
            self.name = name
            self.value = value

    flight = Flight.objects.get(pk=flightId)
    details = [Detail("From", flight.startAirport), Detail("To", flight.endAirport),
               Detail("Departure", flight.startTime), Detail("Arrival", flight.endTime),
               Detail("Airplane registration number", flight.airplane.registerNumber),
               Detail("Number of places", flight.airplane.places),
               Detail("Number of free places", flight.airplane.places - passengers.count())]

    return render(request, 'flight.html', locals())


@require_POST
def register(request):
    if User.objects.all().filter(username=request.POST['username']).exists():
        registerError = True
    else:
        user = User.objects.create_user(
            username=request.POST['username'], password=request.POST['password'])
        login_to_session(request, user)
        registerSuccess = True
    return render(request, 'accountManagement.html', locals())


@require_POST
def login(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login_to_session(request, user)
        loginSuccess = True
    else:
        loginError = True
    return render(request, 'accountManagement.html', locals())


def logout(request):
    if request.user.is_authenticated:
        djangoLogout(request)
        logoutSuccess = True
    else:
        logoutError = True
    return render(request, 'accountManagement.html', locals())

