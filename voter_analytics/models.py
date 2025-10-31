# File: models.py #
# Author: Artemios Kayas (akayas@bu.edu) #
# Description: Models page to hold all my models for the voter_analytics app
from django.db import models

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
        return f'{self.first_name} {self.last_name} {self.party_affiliation}'

def load_data():
    '''Funciton to load data from a file'''
    file_name = '/Users/temi/Downloads/newton_voters.csv'
    file = open(file_name, 'r')

    for i in range(10):
        line = file.readline()
        print(line)