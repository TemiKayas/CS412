from re import I
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random


'''These are my quote and image dictonarys. I thought dictionarys were a good solution for them. '''
global_quotes = {
    "quote1": {
        "text": "You have power over your mind - not outside events. Realize this, and you will find strength.",
        "author": "Marcus Aurelius"
    },
    "quote2": {
        "text": "Dwell on the beauty of life. Watch the stars, and see yourself running with them.",
        "author": "Marcus Aurelius"
    },
    "quote3": {
        "text": "The happiness of your life depends upon the quality of your thoughts.",
        "author": "Marcus Aurelius"
    },
    "quote4": {
        "text": "Everything we hear is an opinion, not a fact. Everything we see is a perspective, not the truth.",
        "author": "Marcus Aurelius"
    },
    "quote5": {
        "text": "Waste no more time arguing about what a good man should be. Be one.",
        "author": "Marcus Aurelius"
    }
}

image_urls = {
    "photo1":{
        "url":"https://cdn.britannica.com/67/148167-050-F596E6F2/Marcus-Aurelius-statue-Rome-Piazza-del-Campidoglio.jpg"
    },
    "photo2":{
        "url":"data:image/jpeg;base64,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"    
    },
    "photo3":{
        "url":"https://art.thewalters.org/images/art/PL1_23.215_Fnt_TR_T97.jpg"
    }
}



def quote(request):
    '''This is the view for the daily quote. It randomly chooses a quote and image from the dictionarys 
    and passes them to the template.'''

    random_quote = random.choice(list(global_quotes.values())) #Chose a random photo and quote
    random_image = random.choice(list(image_urls.values()))
    context = {
        "random_quote": random_quote,
        "image_url": random_image["url"]
    }

    template_name = "quotes/quotes.html"

    return render(request, template_name, context) #Pass in the context to the template

def show_all(request):
    '''This is the view for the all quotes. It passes the quote and image dictionarys to the template.'''
    context = {
        "global_quotes": global_quotes, #load context for the page
        "image_urls": image_urls
    }

    template_name = "quotes/show_all.html"

    return render(request, template_name, context) #Pass in the context to the template
    

def about(request):
    '''This is the view for the about page. it just simply displays information.'''
    context = global_quotes
    
    template_name = "quotes/about.html"

    return render(request, template_name, context) #Pass in the context to the template
    