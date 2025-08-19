from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def about(request):
    return HttpResponse("<h1>About Us</h1><p>This is the about us page. Learn more about our company!</p>")
