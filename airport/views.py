from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import authenticate, login as login_to_session, logout
from django.contrib.auth.models import User
from .models import Flight, Passenger, Ticket, AirplaneCrew, Airplane
from datetime import datetime
from django.db.models import Value as V, Q, Count
from django.db.models.functions import Concat
from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


@require_GET
@csrf_exempt
def get_flights_and_crews(request):
    return JsonResponse({
        'crews': list(AirplaneCrew.objects.all()
                      .annotate(name=Concat('captainsName', V(" "), 'captainsSurname')).values('name')),
        'flights': list(Flight.objects.values('id', 'startAirport', 'endAirport', 'startTime', 'endTime'))
    })


@require_GET
@csrf_exempt
def get_crews(request):
    if 'day' not in request.GET or 'month' not in request.GET or 'year' not in request.GET:
        raise PermissionDenied

    response = []
    filteredFlights = Flight.objects.filter(
        Q(startTime__day=request.GET['day'], startTime__month=request.GET['month'],
          startTime__year=request.GET['year']) |
        Q(endTime__day=request.GET['day'], endTime__month=request.GET['month'],
          endTime__year=request.GET['year']))
    for flight in filteredFlights.filter(crew__isnull=False):
        response.append({'flightId': flight.pk, 'crew': flight.crew.captainsName + " " + flight.crew.captainsSurname})
    return JsonResponse({'crews': response})


@require_POST
@csrf_exempt
def change_flight_crew(request):
    if 'flightId' not in request.POST or 'captainsName' not in request.POST or 'captainsSurname' not in request.POST:
        raise PermissionDenied

    crew = AirplaneCrew.objects.filter(captainsName=request.POST['captainsName'],
                                       captainsSurname=request.POST['captainsSurname'])
    flight = Flight.objects.filter(pk=request.POST['flightId'])
    if not crew.exists() or not flight.exists():
        raise PermissionDenied

    flight = flight[0]
    flight.crew = crew[0]
    try:
        flight.full_clean()
        flight.save()
    except ValidationError:
        raise PermissionDenied
    return HttpResponse()


def flights_list(request):
    if request.GET.get('search'):
        search = datetime.strptime(request.GET['search'], '%Y-%m-%d')
        flights = Flight.objects.filter(Q(startTime__day=search.day, startTime__month=search.month) |
                                        Q(endTime__day=search.day, endTime__month=search.month)).order_by('startTime')
    else:
        flights = Flight.objects.all().order_by('startTime')
    return render(request, 'main.html', locals())


def flight(request, flightId):
    flight = get_object_or_404(Flight, pk=flightId)

    tickets = Ticket.objects.filter(flight=flightId)
    passengers = tickets.values('passenger__name', 'passenger__surname').annotate(tickets=Count('passenger'))

    class Detail:
        def __init__(self, name, value):
            self.name = name
            self.value = value

    details = [Detail("Flight id", flight.pk),
               Detail("From", flight.startAirport), Detail("To", flight.endAirport),
               Detail("Departure", flight.startTime), Detail("Arrival", flight.endTime),
               Detail("Airplane registration number", flight.airplane.registerNumber),
               Detail("Number of places", flight.airplane.places),
               Detail("Number of free places", flight.airplane.places - tickets.count())]

    return render(request, 'flight.html', locals())


@transaction.atomic
@require_POST
def buyTicket(request, flightId):
    if request.user.is_authenticated:
        if Passenger.objects.filter(name=request.POST['name'], surname=request.POST['surname']).exists():
            passenger = Passenger.objects.get(name=request.POST['name'], surname=request.POST['surname'])
        else:
            passenger = Passenger.objects.create(name=request.POST['name'], surname=request.POST['surname'])
        t = Ticket(flight=Flight.objects.get(pk=flightId), passenger=passenger)
        try:
            t.full_clean()
            t.save()
        except ValidationError:
            pass
    else:
        return HttpResponseForbidden()
    return redirect('flight', flightId)


@transaction.atomic
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
        logout(request)
        logoutSuccess = True
    else:
        logoutError = True
    return render(request, 'accountManagement.html', locals())

