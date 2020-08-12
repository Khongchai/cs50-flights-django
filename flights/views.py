from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Flight, Airport


def index(request):
    return render(request, "flights/index.html", {
        "Flights": Flight.objects.all()
    })

