from django import forms
from .models import *

class SearchTrainForm(forms.Form):
    start = forms.ModelChoiceField(queryset=Station.objects.all())
    end = forms.ModelChoiceField(queryset=Station.objects.all())
    date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'],
                               help_text="Example date: 2017-06-01 06:00:00",
                               widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S'))

class TicketTripForm(forms.ModelForm):

    class Meta:
        model = TicketTrip
        fields = ('trip_start_station', 'trip_end_station', 'trip_pay_method', 'trip_date')


class PassengerForm(forms.ModelForm):

    class Meta:
        model = Passenger
        fields = ['p_f_name', 'p_l_name', 'billing_address', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')  # Checks for email structure to be valid, ex: 'e.amespizarro@gmail.com'

        emailBase, emailProvider = email.split('@')
        domain, extension = emailProvider.split('.')

        if not extension == 'edu':
            raise forms.ValidationError('Please enter a college email: "example@college.edu" ')

        return email
