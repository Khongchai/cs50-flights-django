from django.db import models

class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"
        
class Flight(models.Model):
    #CASCADE = if delete airport, delete all other related data too.
    #related_name = reverse-order relationship; from an airport, 
    #what are the flights leaving from it.
    #same goes for destination
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def is_valid_flight(self):
        return self.origin != self.destination or self.duration >= 0

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}. Duration: {self.duration}"

class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    #many to many allows for multiple relationships
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"