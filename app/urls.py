from django.contrib import admin
from django.urls import path, re_path
import airport.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', airport.views.flights_list, name='main'),
    re_path(r'flight/([0-9]+)/', airport.views.flight, name="flight"),
    path('login/', airport.views.login, name='login'),
    path('register/', airport.views.register, name='register'),
    path('logout/', airport.views.logout, name='logout'),
    re_path(r'buyTicket/([0-9]+)/', airport.views.buyTicket, name="buyTicket"),
    path('api/get_crews', airport.views.get_crews, name='get_crews'),
    path('api/change_flight_crew', airport.views.change_flight_crew, name='change_flight_crew'),
]
