from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def contact(request):
    return HttpResponse("<h1>Contact Us</h1><p>This is the contact us page. Get in touch with us!</p>")
