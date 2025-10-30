# File: models.py #
# Author: Artemios Kayas (akayas@bu.edu) #
# Description: Models page to hold all my models for the voter_analytics app
from django.db import models
import csv
from datetime import datetime

class Voter(models.Model):
    '''Data structure for the voter model'''

    voter_id = models.CharField(max_length=20, unique=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=20, blank=True)
    street_name = models.CharField(max_length=200, blank=True)
    apartment_number = models.CharField(max_length=20, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2, blank=True)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField(default=0)

    def __str__(self):
        '''Return the string representation of the voter'''
        return f'{self.first_name} {self.last_name} - {self.street_name} (Precinct {self.precinct_number})'

def load_data():
    '''Function to load data from the CSV file'''
    file_path = '/Users/temi/Downloads/newton_voters.csv'

    # Delete existing records to avoid duplicates
    Voter.objects.all().delete()

    # Open and read the CSV file
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)

        voters_created = 0
        for row in reader:
            try:
                # Create a new Voter instance
                voter = Voter(
                    voter_id=row['Voter ID Number'],
                    last_name=row['Last Name'],
                    first_name=row['First Name'],
                    street_number=row['Residential Address - Street Number'],
                    street_name=row['Residential Address - Street Name'],
                    apartment_number=row['Residential Address - Apartment Number'],
                    zip_code=row['Residential Address - Zip Code'],
                    date_of_birth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date(),
                    date_of_registration=datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date(),
                    party_affiliation=row['Party Affiliation'].strip(),
                    precinct_number=row['Precinct Number'],
                    v20state=(row['v20state'].upper() == 'TRUE'),
                    v21town=(row['v21town'].upper() == 'TRUE'),
                    v21primary=(row['v21primary'].upper() == 'TRUE'),
                    v22general=(row['v22general'].upper() == 'TRUE'),
                    v23town=(row['v23town'].upper() == 'TRUE'),
                    voter_score=int(row['voter_score'])
                )
                voter.save()
                voters_created += 1

            except Exception as e:
                print(f"Error processing row: {e}")
                continue

    print(f"Successfully loaded {voters_created} voters into the database.")
    return voters_created