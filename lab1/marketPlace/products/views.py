from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("<h1>Welcome to Products Page</h1><p>This is the products index page.</p>")
