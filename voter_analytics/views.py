# File: views.py
# Author: Artemios Kayas (akayas@bu.edu)
# Description: Views for the voter_analytics app

from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Q
import plotly.graph_objects as go
from plotly.offline import plot
from collections import Counter

class VoterListView(ListView):
    '''View to display a list of voters with filtering options'''
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        '''Filter the queryset based on GET parameters'''
        queryset = Voter.objects.all().order_by('last_name', 'first_name')

        # Filter by party affiliation
        party = self.request.GET.get('party_affiliation')
        if party:
            queryset = queryset.filter(party_affiliation=party)

        # Filter by minimum date of birth (birth year)
        min_birth_year = self.request.GET.get('min_birth_year')
        if min_birth_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_birth_year))

        # Filter by maximum date of birth (birth year)
        max_birth_year = self.request.GET.get('max_birth_year')
        if max_birth_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_birth_year))

        # Filter by voter score
        voter_score = self.request.GET.get('voter_score')
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))

        # Filter by elections voted in
        if self.request.GET.get('v20state'):
            queryset = queryset.filter(v20state=True)
        if self.request.GET.get('v21town'):
            queryset = queryset.filter(v21town=True)
        if self.request.GET.get('v21primary'):
            queryset = queryset.filter(v21primary=True)
        if self.request.GET.get('v22general'):
            queryset = queryset.filter(v22general=True)
        if self.request.GET.get('v23town'):
            queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        '''Add additional context for the template'''
        context = super().get_context_data(**kwargs)

        # Get distinct party affiliations
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')

        # Generate year ranges for birth year dropdowns
        # Get min and max birth years from database
        birth_years = Voter.objects.dates('date_of_birth', 'year')
        if birth_years:
            min_year = birth_years.first().year
            max_year = birth_years.last().year
            context['birth_years'] = range(min_year, max_year + 1)
        else:
            context['birth_years'] = []

        # Voter scores (0-5)
        context['voter_scores'] = range(0, 6)

        # Preserve filter values in context for form repopulation
        context['selected_party'] = self.request.GET.get('party_affiliation', '')
        context['selected_min_year'] = self.request.GET.get('min_birth_year', '')
        context['selected_max_year'] = self.request.GET.get('max_birth_year', '')
        context['selected_score'] = self.request.GET.get('voter_score', '')
        context['selected_v20state'] = self.request.GET.get('v20state', '')
        context['selected_v21town'] = self.request.GET.get('v21town', '')
        context['selected_v21primary'] = self.request.GET.get('v21primary', '')
        context['selected_v22general'] = self.request.GET.get('v22general', '')
        context['selected_v23town'] = self.request.GET.get('v23town', '')

        return context


class VoterDetailView(DetailView):
    '''View to display details for a single voter'''
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

    def get_context_data(self, **kwargs):
        '''Add additional context for the template'''
        context = super().get_context_data(**kwargs)

        # Create Google Maps URL for the voter's address
        voter = self.object
        address_parts = [
            voter.street_number,
            voter.street_name,
            voter.apartment_number,
            voter.zip_code
        ]
        address = ' '.join([part for part in address_parts if part])
        context['google_maps_url'] = f"https://www.google.com/maps/search/?api=1&query={address.replace(' ', '+')}"

        return context


class GraphsView(ListView):
    '''View to display graphs of voter data with filtering options'''
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        '''Filter the queryset based on GET parameters (reuse from VoterListView)'''
        queryset = Voter.objects.all().order_by('last_name', 'first_name')

        # Filter by party affiliation
        party = self.request.GET.get('party_affiliation')
        if party:
            queryset = queryset.filter(party_affiliation=party)

        # Filter by minimum date of birth (birth year)
        min_birth_year = self.request.GET.get('min_birth_year')
        if min_birth_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_birth_year))

        # Filter by maximum date of birth (birth year)
        max_birth_year = self.request.GET.get('max_birth_year')
        if max_birth_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_birth_year))

        # Filter by voter score
        voter_score = self.request.GET.get('voter_score')
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))

        # Filter by elections voted in
        if self.request.GET.get('v20state'):
            queryset = queryset.filter(v20state=True)
        if self.request.GET.get('v21town'):
            queryset = queryset.filter(v21town=True)
        if self.request.GET.get('v21primary'):
            queryset = queryset.filter(v21primary=True)
        if self.request.GET.get('v22general'):
            queryset = queryset.filter(v22general=True)
        if self.request.GET.get('v23town'):
            queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        '''Add graphs and filter context to the template'''
        context = super().get_context_data(**kwargs)

        # Get filtered voters
        voters = self.get_queryset()

        # Graph 1: Histogram of voters by birth year
        birth_years = [voter.date_of_birth.year for voter in voters]
        year_counts = Counter(birth_years)
        sorted_years = sorted(year_counts.keys())

        fig1 = go.Figure(data=[
            go.Bar(x=sorted_years, y=[year_counts[year] for year in sorted_years])
        ])
        fig1.update_layout(
            title='Distribution of Voters by Birth Year',
            xaxis_title='Year of Birth',
            yaxis_title='Number of Voters'
        )
        context['birth_year_graph'] = plot(fig1, output_type='div')

        # Graph 2: Pie chart of voters by party affiliation
        parties = [voter.party_affiliation if voter.party_affiliation else 'Unknown' for voter in voters]
        party_counts = Counter(parties)

        fig2 = go.Figure(data=[
            go.Pie(labels=list(party_counts.keys()), values=list(party_counts.values()))
        ])
        fig2.update_layout(title='Distribution of Voters by Party Affiliation')
        context['party_graph'] = plot(fig2, output_type='div')

        # Graph 3: Histogram of election participation
        elections = {
            '2020 State': sum(1 for v in voters if v.v20state),
            '2021 Town': sum(1 for v in voters if v.v21town),
            '2021 Primary': sum(1 for v in voters if v.v21primary),
            '2022 General': sum(1 for v in voters if v.v22general),
            '2023 Town': sum(1 for v in voters if v.v23town)
        }

        fig3 = go.Figure(data=[
            go.Bar(x=list(elections.keys()), y=list(elections.values()))
        ])
        fig3.update_layout(
            title='Voter Participation by Election',
            xaxis_title='Election',
            yaxis_title='Number of Voters'
        )
        context['election_graph'] = plot(fig3, output_type='div')

        # Add filter context (same as VoterListView)
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')

        birth_years_qs = Voter.objects.dates('date_of_birth', 'year')
        if birth_years_qs:
            min_year = birth_years_qs.first().year
            max_year = birth_years_qs.last().year
            context['birth_years'] = range(min_year, max_year + 1)
        else:
            context['birth_years'] = []

        context['voter_scores'] = range(0, 6)

        # Preserve filter values
        context['selected_party'] = self.request.GET.get('party_affiliation', '')
        context['selected_min_year'] = self.request.GET.get('min_birth_year', '')
        context['selected_max_year'] = self.request.GET.get('max_birth_year', '')
        context['selected_score'] = self.request.GET.get('voter_score', '')
        context['selected_v20state'] = self.request.GET.get('v20state', '')
        context['selected_v21town'] = self.request.GET.get('v21town', '')
        context['selected_v21primary'] = self.request.GET.get('v21primary', '')
        context['selected_v22general'] = self.request.GET.get('v22general', '')
        context['selected_v23town'] = self.request.GET.get('v23town', '')

        return context
