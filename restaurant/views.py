from re import I
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
import random
# Create your views here.

def main(request):
    template_name = "restaurant/main.html"
    return render(request, template_name)

def order(request):
    
    specials_list = [
        "Tzatziki sauce with extra garlic",
        "Fried potato balls with cheese and bacon",
        "Lemon and rice chicken soup",
        "Stuffed peppers with rice and beef",
        "Greek salad with feta cheese",
        "Cheesy fries with bacon",
    ]
    
    context = {
        "daily_special": random.choice(specials_list)
    }
    template_name = "restaurant/order.html"
    return render(request, template_name, context)

def confirmation(request):
    template_name = "restaurant/confirmation.html"    
    return render(request, template_name)