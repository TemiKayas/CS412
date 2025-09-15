from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time

def home(request):

    funnyvar = "This is a funny variable"

    response_text = f'''
    <html>
    <h1> Hello, World! </h1>
    <p> This is a test response. </p>
    <p> {funnyvar} </p>
    </html>
    
    
    '''
    return HttpResponse(response_text)

def home_page(request):
    #Well do the quotes like this 
    context = {
        "time": time.ctime(),
        "funnymonkeyvar": "This is a funny monkey variable ooo ooo aa aa",
    }

    template_name = "hw/home.html"

    return render(request, template_name, context) #Pass in the context to the template

def about(request):
    #Well do the quotes like this 
    context = {
        "time": time.ctime(),
        "funnymonkeyvar": "This is a funny monkey variable ooo ooo aa aa",
    }

    template_name = "hw/about.html"

    return render(request, template_name, context) #Pass in the context to the template