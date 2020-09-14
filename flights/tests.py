from django.test import TestCase, Client
from flights.models import Airport, Flight, Passenger
from django.db.models import Max

# Create your tests here.
class FlightTestCase(TestCase):

    def setUp(self):

        #create airports.
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        #create flights.
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=1000)

    
    def test_departures_count(self):
        """check number of departures"""
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)


    def test_arrivals_count(self):
        """check number of the "arrivals" related key"""
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    
    def test_valid_flight(self):
        """check if flight is valid >> result should be True"""
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())


    def test_invalid_flight(self):
        """check if flight is invalid >> result should not be False"""
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())
    
    def test_index(self):
        """check status code and contexts; test index page"""
        c = Client()
        response = c.get("/flights/")
        self.assertEqual(response.status_code, 200)

        #check if number of contexts passed is correct
        self.assertEqual(response.context["Flights"].count(), 3)

    def test_valid_flight_page(self):
        """"check flight page"""
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)


    def test_invalid_flight_page(self):
        """check for invalid flights with id out of bound """
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]
        max_id_over = max_id + 1
        c = Client()
        response = c.get(f"/flights/{max_id_over}")
        self.assertEqual(response.status_code, 404)


    def test_flight_page_passengers(self):
        """check number of passengers in a flight"""
        f = Flight.objects.get(pk=0)
        p = Passenger.objects.create(first="Alice", last="Adams")
        f.passengers.add(p)
        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_fligth_page_non_passengers(self):
        """check number of passengers not in a flight"""
        f = Flight.objects.get(pk=0)
        p = Passenger.objects.create(first="Alice", last="Liddel")
        
        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)