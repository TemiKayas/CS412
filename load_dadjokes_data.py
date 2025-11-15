"""
Script to load initial jokes and pictures into the dadjokes app.
Run with: pipenv run python load_dadjokes_data.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cs412.settings')
django.setup()

from dadjokes.models import Joke, Picture

# Add Jokes
jokes_data = [
    {
        "text": "An escalator can never break — it can only become stairs. You should never see 'Escalator temporarily out of order,' just 'Escalator temporarily stairs.'",
        "contributor_name": "Mitch Hedberg"
    },
    {
        "text": "I was going to sail around the globe in the world's smallest ship, but I bottled it.",
        "contributor_name": "Mark Simons"
    },
    {
        "text": "A doctor gave his patient six months to live…but he couldn't pay his bill, so he gave him another six months.",
        "contributor_name": "Henny Youngman"
    },
    {
        "text": "I used to think the brain was the most fascinating part of the body. Then I realized, well…look what's telling me that.",
        "contributor_name": "Emo Philips"
    },
    {
        "text": "What do you call batman when he skips church? Christian Bale!",
        "contributor_name": "Artemios Kayas"
    }
]

# Add Pictures
pictures_data = [
    {
        "image_url": "https://media.istockphoto.com/id/1160791767/photo/laughing-horse.jpg?s=612x612&w=0&k=20&c=_63iHrEConkZdSHORyIjOl7N4R4hxwKCZrwXmt8wptw=",
        "contributor_name": "iStock"
    },
    {
        "image_url": "https://i.pinimg.com/564x/a9/c2/dc/a9c2dc88da90a75c10ee66860eee6fd2.jpg",
        "contributor_name": "Pinterest"
    },
    {
        "image_url": "https://images.unsplash.com/photo-1485981133625-f1a03c887f0a?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8c2lsbHl8ZW58MHx8MHx8fDA%3D&fm=jpg&q=60&w=3000",
        "contributor_name": "Pinterest"
    },
    {
        "image_url": "https://play-lh.googleusercontent.com/jTLd932Uf3QIPmueUYPJQ6mXEhm4qW5RP2SlGVAQoHnI97Ssl12O8fIgH0Qtg7FpnR8=w240-h480-rw",
        "contributor_name": "Google Play"
    },
    {
        "image_url": "https://wordpress.wbur.org/wp-content/uploads/2018/10/1016_comedy-wildlife01-1000x666.jpg",
        "contributor_name": "Google"
    }
]

# Create jokes
print("Adding jokes...")
for joke_data in jokes_data:
    joke = Joke.objects.create(**joke_data)
    print(f"Added joke by {joke.contributor_name}")

# Create pictures
print("\nAdding pictures...")
for picture_data in pictures_data:
    picture = Picture.objects.create(**picture_data)
    print(f"Added picture from {picture.contributor_name}")

print("\nDone! All jokes and pictures have been added to the database.")
print(f"Total jokes: {Joke.objects.count()}")
print(f"Total pictures: {Picture.objects.count()}")
