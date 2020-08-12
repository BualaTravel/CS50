from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
# def index(request):    #this request is the HTTP request the user made
#     return HttpResponse("Hello!")

#now I do not want to only display a big string but an HTML TEMPLATE
def index(request):
    return render(request, "hello/index.html")

def crystian(request):
    return HttpResponse("Hello, Crystian!")

# def greet(request, name):
#     return HttpResponse(f"Hello, {name.capitalize()}!")

def greet(request, name):
    return render(request, "hello/greet.html", {     #render automatically go an check in templates folder
    "name":name.capitalize()
    })
