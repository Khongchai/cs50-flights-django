from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Flight, Airport


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
        return HttpResponse("Error, flight does not exist")
    
    return render(request, "flights/flight.html", {
        "flight": flight,
        #access passengers through related name; follow the arrow back to its origin
        "passengers": flight.passengers.all()
    })

