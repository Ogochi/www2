from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST


def flights_list(request):
    return render(request, 'flight.html')


def flight(request, flightId):
    return HttpResponse("Flight")


@require_POST
def register(request):
    return HttpResponse("Register")


@require_POST
def login(request):
    return HttpResponse("Login")


def logout(request):
    return HttpResponse("Logout")

