from re import I
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
# Create your views here.
def main(request):
    response_text = "This is the main page"
    
    return HttpResponse(response_text)

def order(request):
    response_text = "This is the order page"
    
    return HttpResponse(response_text)

def confirmation(request):
    response_text = "This is the confirmation page"
    
    return HttpResponse(response_text)