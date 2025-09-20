from re import I
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
import random
import time
# Create your views here.

def main(request):
    '''Home page that shows the image and name of the restaurant'''
    template_name = "restaurant/main.html"
    return render(request, template_name)

def order(request):
    '''Order page that shows the daily special and the pizza options'''
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
    '''Confirmation page that shows the order details and gets the form data'''
    template_name = "restaurant/confirmation.html"    

    if request.POST:

        special = request.POST.get("special", "")
        pizzas = request.POST.getlist("pizza") 
        toppings = request.POST.getlist("toppings")  
        special_instructions = request.POST.get("special_instructions", "")
        name = request.POST.get("name", "")
        phone = request.POST.get("phone", "")
        address = request.POST.get("address", "")

        total = 0
        
        if special:
            total += 8.99
            
        total += len(pizzas) * 12.99
            
        total += len(toppings) * 1.50

        ready_minutes = random.randint(30, 60)

        context = {
            "special": special,
            "pizzas": pizzas,
            "toppings": toppings,
            "special_instructions": special_instructions,
            "name": name,
            "phone": phone,
            "address": address,
            "total": total,
            "ready_minutes": ready_minutes,
        }
        
        return render(request, template_name, context)
    
    return render(request, template_name)