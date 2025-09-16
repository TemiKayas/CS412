from re import I
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
# Create your views here.

def main(request):
    template_name = "restaurant/main.html"
    return render(request, template_name)

def order(request):
    template_name = "restaurant/order.html"
    return render(request, template_name)

def confirmation(request):
    template_name = "restaurant/confirmation.html"    
    return render(request, template_name)