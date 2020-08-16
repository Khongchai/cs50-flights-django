from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "users/users.html")
def login_view(request):
    #post = user logs in
    #get = load page
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            #log this user in with this request.
            login(request, user)
            #redirect back to the index function
            return HttpResponseRedirect(reverse("users:index"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid credentials."
            })
    return render(request, "users/login.html")

def logout_view(request):
    #basically just sign the user out
    logout(request)
    #then we decide later where to redirect the users
    return render(request, "users/login.html", {
        "message": "Logged Out."
    })