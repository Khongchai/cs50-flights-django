from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from flights.models import Flight, Airport, Passenger
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    return render(request, "flights/index.html", {
        "Flights": Flight.objects.all()
    })

def flight(request, flight_id):
    #pk = primary key, whatever it is called
    try:
        #create an object of Flight whose id equals flight ID
        flight = Flight.objects.get(pk=flight_id)
    except:
        return HttpResponse("Error, flight does not exist", status=404)
    onboardPassengers = flight.passengers.all()
    otherPassengers = Passenger.objects.exclude(flights=flight).all()

    
    return render(request, "flights/flight.html", {
        "flight": flight,
        #access passengers through related name; follow the arrow back to its origin
        "passengers": onboardPassengers,
        "non_passengers": otherPassengers
    })


def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flights:flight", args=[flight.id]))


